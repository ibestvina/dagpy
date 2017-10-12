import utils
import json


class DAG:

    block_attributes = ['block_id', 'parents', 'description', 'file', 'filter']

    def __init__(self, dag_dict):
        self._dag_dict = dag_dict
        self._reset_parents_and_children()

    def _reset_parents_and_children(self):
        self._parents = {}
        for block_id, block in self._dag_dict['blocks'].items():
            self._parents[block_id] = block['parents']
        self._children = utils.invert_dict(self._parents)

    def block_ids(self):
        return self._dag_dict['blocks']

    def block_cnt(self):
        return len(self._dag_dict['blocks'])

    def get_id(self): return self._dag_dict['id']

    def get_block_att(self, block_id, att_name, default = None):
        block_meta =  self.get_block_metadata(block_id)
        if att_name not in block_meta:
            if default is not None:
                return default
            print('[DAG] Block id', block_id, 'does not contain', att_name)
            return None
        return block_meta[att_name]

    def get_block_metadata(self, block_id):
        if block_id not in self._dag_dict['blocks']:
            print('[DAG] Block id', block_id, 'does not exist')
            return None
        return self._dag_dict['blocks'][block_id]

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

    def update_blocks(self, blocks_meta):
        for block_meta in blocks_meta:
             self.update_block(block_meta, recalculate_support = False)
        self._reset_parents_and_children()

    def update_block(self, block_meta, recalculate_support = True):
        block_id = block_meta['block_id']
        for block_att in DAG.block_attributes:
            self._dag_dict['blocks'][block_id][block_att] = block_meta[block_att]
        if recalculate_support:
            self._reset_parents_and_children()


    @staticmethod
    def from_file(fpathname):
        dag_dict = json.load(open(fpathname))
        return DAG(dag_dict)
