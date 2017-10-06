import utils
import os.path


class DAGExecutor:

    def __init__(self, dag, path):
        self._dag = dag
        self._path = path
        self._cex = utils.Console_executor()

    def _run_ipynb_command(self, block_id):
        #filename = utils.block_filename(self._dag.get_id(), block_id)
        fname = self._dag.block_filename(block_id)
        fpathname = os.path.join(self._path, fname)
        return 'jupyter nbconvert --ExecutePreprocessor.timeout=-1 --execute --inplace ' + fpathname

    def _execute_block(self, block_id):
        command = self._run_ipynb_command(block_id)
        print('Executing', block_id)
        self._cex.run(command, block_id)

    def execute_blocks(self, block_ids):
        pending_to_execute = utils.all_dependencies(self._dag, block_ids)
        pending_parents_cnt = {block_id: len(self._dag.parents_of(block_id)) for block_id in pending_to_execute}
        block_cnt = self._dag.block_cnt()
        while pending_to_execute or self._cex.run_cnt():
            # print('pending', pending_to_execute)
            # print('parent_cnt', pending_parents_cnt)
            # print('running', self._cex.run_cnt())
            print('Executed {}/{} blocks'.format(block_cnt - len(pending_to_execute), block_cnt))
            execute_now = [block_id for block_id in pending_to_execute if not pending_parents_cnt[block_id]]
            for block_id in execute_now:
                pending_to_execute.remove(block_id)
                self._execute_block(block_id)
            
            if self._cex.run_cnt():
                retval = self._cex.blocking_poll(0.1)
                if retval['retcode'] != 0:
                    print('Error executing block', retval['proc_id'])
                    print('Execution output:\n', retval['output'].read())
                for child_id in self._dag.children_of(retval['proc_id']):
                    if child_id in pending_parents_cnt: pending_parents_cnt[child_id] -= 1
