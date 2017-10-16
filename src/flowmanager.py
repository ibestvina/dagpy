import utils
import blockio

import dag
import os
import re

import nbformat
from nbformat.v4 import new_markdown_cell, new_code_cell, new_notebook

class FlowManager:
    """Manages the creation, parsing and saving of flow notebooks""" 

    def __init__(self, dag, path):
        """Init from DAG object used for block lookup and .dagpy path to which block files are relative."""
        self._dag = dag
        self._path = path

    @staticmethod
    def read_nb(fpathname):
        """Read the iPython notebook file."""
        with open(fpathname, encoding='utf-8') as f:
            return nbformat.read(f, as_version=4)

    def _read_block_nb(self, block_id):
        """Read the block notebook file."""
        fname = self._dag.block_filename(block_id)
        fpathname = os.path.join(self._path, fname)
        return self.read_nb(fpathname)

    def _header_cell(self):
        """Create the header cell with custom DAGpy code, such as the start_new_dagpy_block function.
        Header cell is loaded from the header_cell.py file.
        """
        source = open("header_cell.py").read()
        return new_code_cell(source = source, metadata = {'dagpy': {'cell_type': blockio.HEADER_CELL_TYPE}})

    def _delimiter_cell(self, block_id):
        """Delimiter cell between blocks, specifying the following block metadata."""
        source = '### Block_id\n' + str(block_id) + '\n'
        source += '##### Description\n' + self._dag.get_block_att(block_id, 'description', default='') + '\n'
        source += '##### Parents\n' + ', '.join(self._dag.get_block_att(block_id, 'parents', default='')) + '\n'
        source += '##### Filter\n' + ', '.join(self._dag.get_block_att(block_id, 'filter', default='')) + '\n'
        source += '##### File\n' + self._dag.get_block_att(block_id, 'file', default='')
        return new_markdown_cell(source=source, metadata={'dagpy': {'cell_type': blockio.DELIMITER_CELL_TYPE, 'block_id': block_id}})

    def _create_notebook(self):
        """Create new flow notebook with title and header cells"""
        title_cell = new_markdown_cell(source='## DAGpy Flow notebook\nIf you want to start a new block, just run the start_new_dagpy_block() in the cell!', metadata={'dagpy': {'cell_type': blockio.TITLE_CELL_TYPE}})
        return new_notebook(cells=[self._header_cell(), title_cell])

    def merge_blocks(self, block_ids):
        """Merge blocks into a flow notebook."""
        merged = self._create_notebook()
        for block_id in block_ids:
            nb = self._read_block_nb(block_id)
            merged.cells.append(self._delimiter_cell(block_id))
            merged.cells.extend(nb.cells)
        merged.metadata.name = "dagpy_flow"
        return merged

    def flow_to_file(self, block_ids, filepathname):
        """Create flow and save it to file."""
        block_ids_linearized = utils.linearize_dependencies(self._dag, block_ids)
        nb = self.merge_blocks(block_ids_linearized)
        nbformat.write(nb, filepathname)


    @staticmethod
    def parse_delimiter_cell_att(att_name, lines):
        """Parse a single block attribute from a delimiter cell."""
        if att_name == 'block_id':
            return re.sub( '\s+', '', ''.join(lines))
        if att_name == 'description':
            return '\n'.join(lines)
        if att_name == 'file':
            return ''.join([line.strip() for line in lines])
        if att_name in ['parents', 'filter']:
            return re.sub( '[,\s]+', ' ', ' '.join(lines)).split()


    @staticmethod
    def parse_delimiter_cell(cell):
        """Parse a delimiter cell to retrieve block metadata attributes."""
        block_meta = {}
        lines = cell.source.splitlines()
        att_name = None
        att_lines = []
        for line in lines:  
            if line and line[0] == '#':
                if att_name:
                    block_meta[att_name] = FlowManager.parse_delimiter_cell_att(att_name, att_lines)

                att_name = re.sub( '[#\s]+', '', line).strip().lower()
                att_lines = []
            elif att_name:
                att_lines += [line]
        if att_name:
            block_meta[att_name] = FlowManager.parse_delimiter_cell_att(att_name, att_lines)

        if 'block_id' in cell.metadata['dagpy']:
            # preexisting block
            if 'block_id' in block_meta and block_meta['block_id'] != cell.metadata['dagpy']['block_id']:
                # user has changed the block id
                # TODO: Decide if block_id can be changed in flow. Probably not.
                block_meta['block_id'] = cell.metadata['dagpy']['block_id']
            else:
                block_meta['block_id'] = cell.metadata['dagpy']['block_id']
        else:
            # new block
            if 'block_id' not in block_meta:
                print('ERROR: no block_id specified')
                block_meta['block_id'] = 'new_block'
        
        return block_meta


    def apply_flow_changes(self, filepathname):
        """Apply changes made in the flow to block files and the DAG."""
        cells = self.read_nb(filepathname).cells
        blocks_to_save = {}
        block_cells = []
        block_meta = {}
        blocks_meta = []
        for cell in cells:
            if 'dagpy' in cell.metadata:
                if cell.metadata['dagpy']['cell_type'] == blockio.DELIMITER_CELL_TYPE:  # other dagpy cell types are ignored
                    if block_meta:
                        blocks_meta += [block_meta]
                        blocks_to_save[block_meta['block_id']] = block_cells
                        block_cells = []
                    block_meta = FlowManager.parse_delimiter_cell(cell)
            else:
                block_cells += [cell]

        if block_meta:
            blocks_meta += [block_meta]
            blocks_to_save[block_meta['block_id']] = block_cells

        if blocks_meta:
            self._dag.update_blocks(blocks_meta)

        for block_id, block_cells in blocks_to_save.items():
            blockio.save_block(block_id, block_cells, self._dag)
