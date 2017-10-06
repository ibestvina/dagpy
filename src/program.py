import dag
import dagexecutor
import flowmanager

dagpy_filepath = 'playground/dag_example_1.txt'

mydag = dag.DAG.from_file(dagpy_filepath)
mydagex = dagexecutor.DAGExecutor(mydag, '')
mydagex.execute_blocks(['D'])
#myflowmng = flowmanager.FlowManager(mydag, '')
#nb = myflowmng.merge_notebooks(['A','D'])