import utils
import dag
import os

import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

class FlowManager:
    TITLE_BLOCK_ID = '_dagpy_title_block'

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
        source = '### Block_id\n' + str(block_id)
        source += '#### Parents\n' + '\n'.join(self._dag.parents_of(block_id))
        return new_markdown_cell(source=source, metadata={'dagpy': {'block_id': block_id}})

    def _create_notebook(self):
        title_cell = new_markdown_cell(source='## DAGpy Flow notebook', metadata={'dagpy': {'block_id': TITLE_BLOCK_ID}})
        return new_notebook(cells=[title_cell])

    def merge_notebooks(self, block_ids):
        merged = self._create_notebook()
        for block_id in block_ids:
            nb = self._read_block_nb(block_id)
            merged.cells.append(self._delimiter_cell(block_id))
            merged.cells.extend(nb.cells)
        merged.metadata.name = "dagpy_flow"
        return merged

    def flow_to_file(self, block_ids, filepathname):
        block_ids_linearized = utils.linearize_dependencies(self._dag, block_ids)
        nb = self.merge_notebooks(block_ids_linearized)
        nbformat.write(nb, filepathname)

    """
    @staticmethod
    def parse_dagpy_cell():
        return {}

    def apply_flow_changes(self, filepathname):
        nb = read_nb(filepathname)
        blocks = []
        block_nb = None
        while nb.cells:
            cell = nb.cells.pop(0)
            if 'dagpy' in cell.metadata:
                if block_nb is None:
                    block_nb = new_notebook(cells = [cell])
                    continue
                block_id = cell.metadata['dagpy']['block_id']
                if block_id != TITLE_BLOCK_ID:
                    block_dict = parse_dagpy_cell(cell)
                    self._dag.update_block(block_id, block_nb, block_dict)
                block_nb = new_notebook()
            else
                block_nb.cells.append(cell)
    """
