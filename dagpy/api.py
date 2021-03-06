

def check_blocks(dag, block_ids):
    """Check if all blocks exist"""
    if set(block_ids) - set(dag.block_ids()):
        return False
    return True

def execute_blocks(dag_fpathname, block_ids, exec_all=False):
    """Execute blocks passed and all their dependencies"""
    from . import dag
    from . import dagexecutor

    d = dag.DAG.from_file(dag_fpathname)
    if exec_all: block_ids = d.block_ids()
    else:
        nonexistent = set(block_ids) - set(d.block_ids())
        if nonexistent:
            print('Block(s) {} have not been found.'.format(nonexistent))
            return
    dex = dagexecutor.DAGExecutor(d, dag_fpathname)
    dex.execute_blocks(block_ids)


def open_notebook(nbfile):
    """Start the server and run the notebook in the user's prefered browser"""
    from .utils import ConsoleExecutor
    import subprocess

    print('Running {}'.format(nbfile))
    command = 'jupyter notebook ' + nbfile
    subprocess.check_output(command.split())


def create_flow(dag_fpathname, block_ids, flow_name, run=False):
    """Create the flow of passed blocks and their dependencies, and open it if run=True"""
    from . import dag
    from . import flowmanager
    import os

    d = dag.DAG.from_file(dag_fpathname)
    flow = flowmanager.FlowManager(d, os.path.dirname(dag_fpathname))
    flow_fname = flow_name
    if not flow_fname.endswith('.ipynb'): flow_fname += '.ipynb'
    flow.flow_to_file(block_ids, flow_fname)
    if run: open_notebook(flow_fname)


def update_from_flow(dag_fpathname, flow_fpathname):
    """Update block files and the DAG with the changes made in the flow."""
    from . import dag
    from . import flowmanager

    d = dag.DAG.from_file(dag_fpathname)
    flow = flowmanager.FlowManager(d, dag_fpathname)
    flow.apply_flow_changes(flow_fpathname)
    d.to_file(dag_fpathname)


def new_project(project_name, run=False):
    """Create a new project (empty .dagpy file)."""
    from . import dag
    from .utils import ConsoleExecutor

    d = dag.DAG.empty(project_name)
    dag_fpathname = project_name+'.dagpy'
    d.to_file(dag_fpathname)
    
    if run:
        flowname = project_name + '_initialflow.ipynb'
        create_flow(dag_fpathname, [], flowname, run)
        

def display_dag(dag_fpathname, flow = None):
    """Display the DAG in a new window (non-interactive)."""
    from . import dag
    from . import utils

    d = dag.DAG.from_file(dag_fpathname)
    to_color = []
    if flow is not None:
        to_color = utils.all_dependencies(d, flow)
    utils.dag_draw(d, to_color=to_color)


def add_or_update_block(dag_fpathname, block_id, block):
    """Add a new block or update if already exists."""
    from . import dag
    from . import blockio

    d = dag.DAG.from_file(dag_fpathname)
    is_new = d.add_or_update_block(block_id, block)
    d.to_file(dag_fpathname)
    if is_new: blockio.save_block(block_id, [], d)


def add_block(dag_fpathname, block_id, block):
    """Add a new block, overwrite if already exists."""
    import dag
    import blockio

    d = dag.DAG.from_file(dag_fpathname)
    d.add_block(block_id, block)
    d.to_file(dag_fpathname)
    blockio.save_block(block_id, [], d)


def update_block(dag_fpathname, block_id, block):
    """Update block, do nothing if it doesn't exist."""
    from . import dag
    from . import blockio

    block['block_id'] = block_id
    d = dag.DAG.from_file(dag_fpathname)
    if block_id not in d.block_ids():
        print('Block {} was not found.'.format(block_id))
        return
    d.update_block(block)
    blockio.save_block(block_id, [], d)


def remove_block(dag_fpathname, block_id):
    """Remove the block from the DAG, but keep the block file."""
    import dag
    import blockio

    d = dag.DAG.from_file(dag_fpathname)
    if block_id not in d.block_ids():
        print('Block {} was not found.'.format(block_id))
        return
    d.remove_block(block_id)
    d.to_file(dag_fpathname)
