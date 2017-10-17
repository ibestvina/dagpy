import os

import nbformat
from nbformat.v4 import new_notebook, new_code_cell


TITLE_CELL_TYPE = 'title'  # flow title cell, markdown, not parsed
DELIMITER_CELL_TYPE = 'delimiter'  # flow delimiter cell, markdown, parsed for block attributes
INPUT_FILTER_CELL_TYPE = 'input_filter'  # input filter cell, code, generated for filter input functionality
OUTPUT_FILTER_CELL_TYPE = 'output_filter'  # output filter cell, code, generated for filter output functionality
HEADER_CELL_TYPE = 'header'  # header cell, code, generated for various dagpy flow functionalities (e.g. start new block)



def filter_file(var_name, block_id, dag):
    """Return path to the filter (.dill) file."""
    # TODO: give users the freedom to choose where and by which name filtered vars is saved.
    return 'cache/{}_{}.dill'.format(str(block_id), str(var_name))
    #return os.path.join('cache', fname)

def placeholder_cell():
    """Create a new code cell with placeholder comment. Used in empty blocks."""
    new_code_cell(source='# Hi, this is an empty DAGpy block. Add your cells here!\n')


def filter_input_cell(block_id, dag):
    """Input filter cell code. Imports dill and loads all of the parents' filtered vars."""
    source_str = '# DAGpy input filter\nimport dill'
    parents = dag.parents_of(block_id)
    for parent in parents:
        pfilter = dag.get_block_att(parent, 'filter', default = [])
        for var_name in pfilter:
            inblock_var_name = '{!s}_{!s}'.format(parent, var_name)
            fpathname = filter_file(var_name, parent, dag)
            source_str += "\n{} = dill.load(open('{!s}','rb'))".format(inblock_var_name, fpathname)
    return new_code_cell(source=source_str, metadata={'dagpy':{'cell_type': INPUT_FILTER_CELL_TYPE}})

def filter_output_cell(block_id, dag):
    """Ouput filter cell code. Imports dill and dumps all of the block's output filter vars."""
    source_str = '# DAGpy output filter\n# To change the filter, edit the block properties, not this cell.\nimport dill\nimport os'
    block_filter = dag.get_block_att(block_id, 'filter', default = [])
    for var_name in block_filter:
        fpathname = filter_file(var_name, block_id, dag)
        source_str += "\nos.makedirs(os.path.dirname('{!s}'), exist_ok=True)".format(fpathname)
        source_str += "\ndill.dump({}, open('{!s}', 'wb+'))".format(var_name, fpathname)
    return new_code_cell(source=source_str, metadata={'dagpy':{'cell_type': OUTPUT_FILTER_CELL_TYPE}})


def save_block(block_id, block_cells, dag):
    """Save the block to the ipynb block file"""
    nb = new_notebook()
    nb.metadata['dagpy'] = {}
    nb.metadata['dagpy']['block_id'] = block_id
    if not block_cells:
        block_cells = [placeholder_cell()]
    nb.cells = [filter_input_cell(block_id, dag)] + block_cells + [filter_output_cell(block_id, dag)]
    fpathname = dag.get_block_att(block_id, 'file', default = '{!s}.ipynb'.format(block_id))
    nbformat.write(nb, fpathname)
