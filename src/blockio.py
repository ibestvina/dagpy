import nbformat
from nbformat.v4 import new_notebook, new_code_cell

def save_block(block_meta, block_cells):
    nb = new_notebook()
    nb.metadata['dagpy'] = {}
    nb.metadata['dagpy']['block_id'] = block_meta['block_id']
    filter_input_cell = new_code_cell(source='# here goes the input filter')
    filter_output_cell = new_code_cell(source='# here goes the output filter of vars: ' + str(block_meta['filter']))
    nb.cells = [filter_input_cell] + block_cells + [filter_cell]
    fpathname = block_meta['file']
    nbformat.write(nb, fpathname)