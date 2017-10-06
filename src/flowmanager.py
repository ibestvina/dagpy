import utils
import dag
import os

from IPython import nbformat
from nbformat.v4 import new_markdown_cell, new_notebook

class FlowManager:
    def __init__(self, dag, path):
        self._dag = dag
        self._path = path

    def _read_nb(self, block_id):
        fname = self._dag.block_filename(block_id)
        fpathname = os.path.join(self._path, fname)
        with open(fpathname, encoding='utf-8') as f:
            return nbformat.read(f, as_version=4)

    def _delimiter_cell(self, block_id):
        return new_markdown_cell(source='Delimiter for block ' + str(block_id))

    def _create_notebook(self):
        title_cell = new_markdown_cell(source='## DAGpy Flow notebook')
        return new_notebook(cells=[title_cell])

    def merge_notebooks(self, block_ids):
        merged = self._create_notebook()
        for block_id in block_ids:
            nb = self._read_nb(block_id)
            merged.cells.append(self._delimiter_cell(block_id))
            merged.cells.extend(nb.cells)
        merged.metadata.name = "dagpy_flow"
        return merged

    def flow_to_file(self, block_ids, filepathname):
        pass
        # nbformat.write(merged, filepathname)