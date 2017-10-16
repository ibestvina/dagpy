import utils
import os.path


class DAGExecutor:
    """Manages the DAG blocks execution and Jupyter kernel communication."""

    def __init__(self, dag, path):
        """Init from DAG object used for block lookup and .dagpy path to which block files are relative."""
        self._dag = dag
        self._path = os.path.dirname(path)
        self._cex = utils.ConsoleExecutor()

    def _run_ipynb_command(self, block_id):
        """Command which runs and updates (inplace) a iPython notebook."""
        # TODO: replace with the iPython API calls.
        #filename = utils.block_filename(self._dag.get_id(), block_id)
        fname = self._dag.block_filename(block_id)
        fpathname = os.path.join(self._path, fname)
        return 'jupyter nbconvert --ExecutePreprocessor.timeout=-1 --execute --inplace ' + fpathname

    def _execute_block(self, block_id):
        """Execute a block."""
        command = self._run_ipynb_command(block_id)
        print('Executing', block_id)
        self._cex.run(command, block_id)

    def execute_blocks(self, block_ids):
        """Execute multiple blocks and all their dependencies."""
        # TODO: check for changes and execute only what needs updating
        pending_to_execute = utils.all_dependencies(self._dag, block_ids)
        pending_parents_cnt = {block_id: len(self._dag.parents_of(block_id)) for block_id in pending_to_execute}
        block_cnt = len(pending_to_execute)

        while pending_to_execute or self._cex.run_cnt():
            print('Executed {}/{} blocks'.format(block_cnt - len(pending_to_execute), block_cnt))
            execute_now = [block_id for block_id in pending_to_execute if not pending_parents_cnt[block_id]]
            for block_id in execute_now:
                pending_to_execute.remove(block_id)
                self._execute_block(block_id)
            
            if self._cex.run_cnt():
                retval = self._cex.blocking_poll(0.1)
                if retval['retcode'] != 0:
                    print('Error executing block {}, retcode: {}'.format(retval['proc_id'], retval['retcode']))
                    print('Execution output:\n', retval['output'].read())
                    print('\n')
                    return
                for child_id in self._dag.children_of(retval['proc_id']):
                    if child_id in pending_parents_cnt: pending_parents_cnt[child_id] -= 1
