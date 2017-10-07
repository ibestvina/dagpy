import utils
import blockio

import dag
import os
import re

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

class FlowManager:

    TITLE_BLOCK_TYPE = 'title'
    DELIMITER_BLOCK_TYPE = 'delimiter'


    def __init__(self, dag, path):
        self._dag = dag
        self._path = path

    @staticmethod
    def read_nb(fpathname):
        with open(fpathname, encoding='utf-8') as f:
            return nbformat.read(f, as_version=4)

    def _read_block_nb(self, block_id):
        fname = self._dag.block_filename(block_id)
        fpathname = os.path.join(self._path, fname)
        return self.read_nb(fpathname)

    def _delimiter_cell(self, block_id):
        source = '### Block_id\n' + str(block_id) + '\n'
        source += '##### Description\n' + self._dag.get_block_att(block_id, 'description', default='') + '\n'
        source += '##### Parents\n' + ', '.join(self._dag.get_block_att(block_id, 'parents', default='')) + '\n'
        source += '##### Filter\n' + ', '.join(self._dag.get_block_att(block_id, 'filter', default='')) + '\n'
        source += '##### File\n' + self._dag.get_block_att(block_id, 'file', default='')

        return new_markdown_cell(source=source, metadata={'dagpy': {'cell_type': FlowManager.DELIMITER_BLOCK_TYPE, 'block_id': block_id}})

    def _create_notebook(self):
        title_cell = new_markdown_cell(source='## DAGpy Flow notebook', metadata={'dagpy': {'cell_type': FlowManager.TITLE_BLOCK_TYPE}})
        return new_notebook(cells=[title_cell])

    def merge_blocks(self, block_ids):
        merged = self._create_notebook()
        for block_id in block_ids:
            nb = self._read_block_nb(block_id)
            merged.cells.append(self._delimiter_cell(block_id))
            merged.cells.extend(nb.cells)
        merged.metadata.name = "dagpy_flow"
        return merged

    def flow_to_file(self, block_ids, filepathname):
        block_ids_linearized = utils.linearize_dependencies(self._dag, block_ids)
        nb = self.merge_blocks(block_ids_linearized)
        nbformat.write(nb, filepathname)


    @staticmethod
    def parse_delimiter_cell_att(att_name, lines):
        if att_name == 'block_id':
            return re.sub( '\s+', '', ''.join(lines))
        if att_name == 'description':
            return '\n'.join(lines)
        if att_name == 'file':
            return ''.join([line.strip() for line in lines])
        if att_name in ['parents', 'filter']:
            return re.sub( '[,\s]+', ' ', ' '.join(lines)).split(' ')


    @staticmethod
    def parse_delimiter_cell(cell):
        block_meta = {'block_id': cell.metadata['dagpy']['block_id']}
        lines = cell.source.splitlines()
        att_name = None
        att_lines = []
        for line in lines:  
            if line and line[0] == '#':
                if att_name:
                    block_meta[att_name] = FlowManager.parse_delimiter_cell_att(att_name, att_lines)
                    if block_meta['block_id'] != cell.metadata['dagpy']['block_id']:
                        # user has changed the block id
                        # TODO: Decide if block_id can be changed in flow. Probably not.
                        block_meta['block_id'] = cell.metadata['dagpy']['block_id']
                att_name = re.sub( '[#\s]+', '', line).strip().lower()
                att_lines = []
            elif att_name:
                att_lines += [line]
        if att_name:
            block_meta[att_name] = FlowManager.parse_delimiter_cell_att(att_name, att_lines)
        return block_meta


    def apply_flow_changes(self, filepathname):
        cells = self.read_nb(filepathname).cells
        block_cells = []
        block_meta = {}
        blocks_meta = []
        for cell in cells:
            if 'dagpy' in cell.metadata:
                if cell.metadata['dagpy']['cell_type'] == FlowManager.DELIMITER_BLOCK_TYPE:  # title cell is ignored
                    if block_meta:
                        blocks_meta += [block_meta]
                        blockio.save_block(block_meta, block_cells)
                        block_cells = []
                    block_meta = FlowManager.parse_delimiter_cell(cell)
            else:
                block_cells += [cell]

        if block_meta:
            blocks_meta += [block_meta]
            blockio.save_block(block_meta, block_cells)

        if blocks_meta:
            self._dag.update_blocks(blocks_meta)

