import utils
import json

class DAG:
        
    def __init__(self, dag_dict):
        self._dag_dict = dag_dict
        self._reset_parents_and_children()

    def _reset_parents_and_children(self):
        self._parents = {}
        for block_id, block in dag_dict['blocks'].items():
            self._parents[block_id] = block['parents']
        self._children = utils.invert_dict(self._parents)

    def block_cnt(self):
        return len(self._dag_dict['blocks'])

    def get_id(self): return self._dag_dict['id']

    def parents_of(self, block_id):
        if block_id not in self._parents:
            return []
        return self._parents[block_id]

    def children_of(self, block_id):
        if block_id not in self._children:
            return []
        return self._children[block_id]

    def add_block(self, block_id, block):
        self._dag_dict['blocks']['block_id'] = block
        self._reset_parents_and_children()

    def remove_block(self, block_id):
        block = self._dag_dict['blocks'][block_id]
        self._reset_parents_and_children()

    def set_parents(self, block_id, parents):
        self._dag_dict['blocks']['parents'] = parents
        self._reset_parents_and_children()

    def block_filename(self, block_id):
        return self._dag_dict['blocks'][block_id]['file']

    def to_file(self, fpath):
        return utils.dict_to_json_file(self._dag_dict, fpath)

    def update_block(self, block_id, block_nb, block_dict):


    @staticmethod
    def from_file(fpathname):
        dag_dict = json.load(open(fpathname))
        return DAG(dag_dict)
