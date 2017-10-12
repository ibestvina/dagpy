

def execute_blocks(dag_fpathname, block_ids):
    import dag
    import dagexecutor

    d = dag.DAG.from_file(dag_fpathname)
    dex = dagexecutor.DAGExecutor(d, dag_fpathname)
    dex.execute_blocks(block_ids)


def create_flow(dag_fpathname, block_ids, flow_fname)
    import dag
    import flowmanager

    d = dag.DAG.from_file(dag_fpathname)
    flow = flowmanager.FlowManager(d, dag_fpathname)
    flow.flow_to_file(block_ids, flow_fname)


def update_from_flow(dag_fpathname, flow_fpathname):
    d = dag.DAG.from_file(dag_fpathname)
    flow = flowmanager.FlowManager(d, dag_fpathname)
    flow.apply_flow_changes(flow_fpathname)
    d.to_file(dag_fpathname)


def new_project(fpath):
    pass


def display_dag(fpathname, flow = None):
    import dag
    import utils

    d = dag.DAG.from_file(fpathname)
    to_color = []
    if flow is not None:
        to_color = utils.all_dependencies(d, flow)
    utils.dag_draw(d, to_color=to_color)
