import dag
import dagexecutor

mydag = dag.DAG.from_file('playground/dag_example_1.txt')
mydagex = dagexecutor.DAGExecutor(mydag, 'D:/Projects/dagpy/src/')
mydagex.execute_blocks(['D'])