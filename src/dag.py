import utils
import os.path


class DAG:
    def from_file(file):
        pass

    def __init__(self, parents, dag_id):
        # self._blocks = list(parents)
        self.id = dag_id
        self._parents = parents
        self._children = utils.invert_dict(parents)

    def parents_of(self, block_id):
        if block_id not in self._parents:
            return []
        return self._parents[block_id]

    def children_of(self, block_id):
        if block_id not in self._children:
            return []
        return self._children[block_id]


class DAG_executor:
    def __init__(self, dag, blocks_path):
        self._dag = dag
        self._blocks_path = blocks_path
        self._cex = utils.Console_executor()

    def _run_ipynb_command(self, block_id):
        filename = utils.block_filename(self._dag.id, block_id)
        return os.path.join(self._blocks_path, filename)

    def _execute_block(self, block_id):
        command = self._run_ipynb_command(block_id)
        self._cex.run(command, block_id)

    def execute_blocks(self, block_ids):
        pending_to_execute = utils.all_dependencies(self._dag, block_ids)
        pending_parents_cnt = {block_id: len(self._dag.parents_of(block_id)) for block_id in pending_to_execute}

        while pending_to_execute or self._cex.run_cnt():
            execute_now = [block_id for block_id in pending_to_execute if not pending_parents_cnt[block_id]]
            for block_id in execute_now:
                pending_to_execute.remove(block_id)
                self._execute_block(block_id)
            
            if self._cex.run_cnt():
                retval = self._cex.blocking_poll(0.1)
                if retval['retcode'] != 0:
                    print('Error executing block', block_id)
                    print('Execution output:\n', retval['output'].read())
                pending_parents_cnt[retval.proc_id] -= 1
