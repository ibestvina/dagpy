import dag
import utils
import dagexecutor
import flowmanager

dagpy_filepath = 'playground/dag_example_1.txt'

mydag = dag.DAG.from_file(dagpy_filepath)
#print(utils.linearize_dependencies(mydag, ['B']))

#mydagex = dagexecutor.DAGExecutor(mydag, '')
#mydagex.execute_blocks(['D'])

#myflowmng = flowmanager.FlowManager(mydag, '')
#nb = myflowmng.flow_to_file(['D'], 'merged.ipynb')

myflowmng = flowmanager.FlowManager(mydag, '')
myflowmng.apply_flow_changes('merged.ipynb')
print(mydag._dag_dict)
