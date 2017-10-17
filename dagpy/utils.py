import subprocess
import time
import json
import os

# save dict to file as json if it was changed and return True. If unchanged, return False
def dict_to_json_file(d, fpath):
    if os.path.isfile(fpath):
        fd = json.load(open(fpath))
        if d == fd:
            return False
    json.dump(d, open(fpath, 'w+'), indent=4)
    return True

def invert_dict(d):
    values = set(val for val_list in d.values() for val in val_list).union(d.keys())
    return dict((new_key, [key for key,value in d.items() if new_key in value]) for new_key in values)


class ConsoleExecutor:
    def __init__(self):
        self._running_procs = []

    def run(self, command, proc_id):
        print(command)
        self._running_procs.append((subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE), proc_id))

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
            # print('waiting')
            time.sleep(time_step)
            retval = self.poll()
        return retval


def default_block_filename(dag_id, block_id):
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

def linearize_dependencies(dag, block_ids):
    pending = all_dependencies(dag, block_ids)
    pending_parents_cnt = {block_id: len(dag.parents_of(block_id)) for block_id in pending}
    result = []
    while pending:
        add_now = [block_id for block_id in pending if not pending_parents_cnt[block_id]]
        result += add_now
        pending.difference_update(add_now)
        for block_id in add_now:
            for child_id in dag.children_of(block_id):
                if child_id in pending_parents_cnt: pending_parents_cnt[child_id] -= 1
    return result


def dag_draw(dag, block_ids = None, to_color = None):
    import networkx as nx
    from matplotlib import pyplot as plt

    if block_ids is None:
        block_ids = dag.block_ids()

    block_ids = set(block_ids)
    levels = {block_id: 0 for block_id in block_ids if not dag.parents_of(block_id)}

    curr_level = set(levels.keys())
    next_level = set()
    level = 1
    while True:
        next_level = set()
        for block_id in curr_level:
            next_level.update(dag.children_of(block_id))
        next_level = next_level & block_ids
        if not next_level: break
        for block_id in next_level:
            levels[block_id] = level
        level += 1
        curr_level = next_level

    level_cnt = [0] * level
    for block_level in levels.values():
        level_cnt[block_level] += 1
    max_per_level = max(level_cnt)

    level_cnt_curr = [0] * level
    pos_dict = {}
    G = nx.DiGraph()
    for block_id, block_level in levels.items():
        x = level_cnt_curr[block_level] + (max_per_level - level_cnt[block_level] ) * 0.5
        level_cnt_curr[block_level] += 1
        y = levels[block_id] * -2
        pos_dict[block_id] = (x,y)
        G.add_edges_from([(parent, block_id) for parent in dag.parents_of(block_id)])

    nx.draw(G, pos = pos_dict, with_labels = True, node_size=1000, node_color='lightgrey', node_shape='s', edge_color='grey')
    if to_color is not None :
        G_color = G.subgraph(to_color)
        nx.draw(G_color, pos = pos_dict, with_labels = True, node_size=1000, node_color='lightskyblue', node_shape='s', edge_color='cornflowerblue')
    plt.show()
