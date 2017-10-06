import subprocess
import time
import json

# save dict d to file f as json if it was changed and return True. If unchanged, return False
def dict_to_json_file(d, fpath):
    with open(fpath) as f:
        fd = json.load(f)
    if d == fd:
        return False
    with open(fpath, 'w') as f:
        json.dump(d, f)
        return True

def invert_dict(d):
    values = set(val for val_list in d.values() for val in val_list).union(d.keys())
    return dict((new_key, [key for key,value in d.items() if new_key in value]) for new_key in values)


class Console_executor:
    def __init__(self):
        self._running_procs = []

    def run(self, command, proc_id):
        self._running_procs.append((subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE), proc_id))

    def run_cnt(self):
        return len(self._running_procs)

    def poll(self):
        for item in self._running_procs:
            proc, proc_id = item
            retcode = proc.poll()
            if retcode is not None: # process finished
                self._running_procs.remove(item)
                return {'proc_id': proc_id, 'retcode': retcode, 'output': proc.stdout}
        return None

    def blocking_poll(self, time_step=0.1):
        retval = self.poll()
        while retval is None:
            time.sleep(time_step)
            retval = self.poll()
        return retval


def block_filename(dag_id, block_id):
    return '{0}_{1}.ipynb'.format(dag_id, block_id)


def all_dependencies(dag, block_ids):
    result = set()    # dict of dependencies with their number of parents as values
    pending = set(block_ids)
    while True:
        next_pending = set()
        for block_id in pending:
            result.add(block_id)
            next_pending.update(dag.parents_of(block_id))
        next_pending.difference_update(result)
        if not next_pending:
            return result
        pending = next_pending

