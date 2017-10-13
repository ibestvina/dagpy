import utils
import json


class DAG:

    block_attributes = ['parents', 'description', 'file', 'filter']

    def __init__(self, dag_dict):
        self._dag_dict = dag_dict
        self._reset_parents_and_children()

    def _reset_parents_and_children(self):
        self._parents = {}
        for block_id, block in self._dag_dict['blocks'].items():
            self._parents[block_id] = block['parents']
        self._children = utils.invert_dict(self._parents)

    def _remove_redundant_parents(self):
        for block_id, block in self._dag_dict['blocks'].items():
            parents = set(block['parents'])
            dep_parents = set()
            for parent in parents:
                deps = set(utils.all_dependencies(self, parent))
                deps.remove(parent)
                dep_parents.update(deps)
            parents -= dep_parents
            self._dag_dict['blocks'][block_id]['parents'] = list(parents)

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
        self._dag_dict['blocks'][block_id] = block
        self._reset_parents_and_children()

    def add_or_update_block(self, block_id, block):
        if block_id in self.block_ids:
            block['block_id'] = block_id
            self.update_block(block)
            return False
        else:
            self.add_block(block_id, block)
            return True

    def add_parents(self, block_id, parents, recalculate_support = True):
        parents = self._dag_dict['blocks'][block_id]['parents'] + parents
        self._dag_dict['blocks'][block_id]['parents'] = list(set(parents))
        if recalculate_support:
            self._reset_parents_and_children()

    def remove_block(self, block_id):
        parents = self.parents_of(block_id)
        for child in self.children_of(block_id):
            self.add_parents(child, parents, recalculate_support = False)
            self._dag_dict['blocks'][child]['parents'].remove(block_id)
        del(self._dag_dict['blocks'][block_id])
        self._remove_redundant_parents()
        self._reset_parents_and_children()

    def set_parents(self, block_id, parents):
        self._dag_dict['blocks'][block_id]['parents'] = parents
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
            if block_att in block_meta:
                self._dag_dict['blocks'][block_id][block_att] = block_meta[block_att]
        if recalculate_support:
            self._reset_parents_and_children()


    @staticmethod
    def from_file(fpathname):
        dag_dict = json.load(open(fpathname))
        return DAG(dag_dict)

    @staticmethod
    def empty(name):
        dag_dict = {'id': name, 'blocks': {}}
        return DAG(dag_dict)
