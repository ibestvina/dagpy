import utils
import json


class DAG:
    """Main DAG class, holding all of the DAG metadata, blocks, and their metadata.
    Does not contain block cells, as these are loaded only when needed.
    By default, none of the changes are saved to the .dagpy file automatically.
    """
    block_attributes = ['parents', 'description', 'file', 'filter']

    def __init__(self, dag_dict):
        """DAG dict holds all of the information about the DAG to simplify .dagpy read/write operations."""
        self._dag_dict = dag_dict
        self._reset_parents_and_children()

    def _reset_parents_and_children(self):
        """Recalculates the DAG children data from parent data.
        Should be called after a batch of DAG updates are finished.
        """
        self._parents = {}
        for block_id, block in self._dag_dict['blocks'].items():
            self._parents[block_id] = block['parents']
        self._children = utils.invert_dict(self._parents)

    def _remove_redundant_parents(self):
        """Removes redundant dependencies.
        For example, if A <- B, B <- C and A <- C, then A is a redundant parent of C.
        """
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
        """Return all block ids."""
        return self._dag_dict['blocks']

    def block_cnt(self):
        """Return the block count."""
        return len(self._dag_dict['blocks'])

    def get_id(self):
        """Return the DAG id"""
        return self._dag_dict['id']

    def get_block_att(self, block_id, att_name, default = None):
        """Get attribute value of the block.
        Return default if specified and att is not found in the block metadata.
        Otherwise print error and return None.
        """
        block_meta =  self.get_block_metadata(block_id)
        if att_name not in block_meta:
            if default is not None:
                return default
            print('[DAG] Block id', block_id, 'does not contain', att_name)
            return None
        return block_meta[att_name]

    def get_block_metadata(self, block_id):
        """Get all of the block's metadata as a dict."""
        if block_id not in self._dag_dict['blocks']:
            print('[DAG] Block id', block_id, 'does not exist')
            return None
        return self._dag_dict['blocks'][block_id]

    def parents_of(self, block_id):
        """Get parents of the block."""
        if block_id not in self._parents:
            return []
        return self._parents[block_id]

    def children_of(self, block_id):
        """Get children of the block."""
        if block_id not in self._children:
            return []
        return self._children[block_id]

    def add_block(self, block_id, block):
        """Add block to the DAG. Does not create or update the block file."""
        self._dag_dict['blocks'][block_id] = block
        self._reset_parents_and_children()

    def add_or_update_block(self, block_id, block):
        """Add block if not in the DAG, update otherwise."""
        if block_id in self.block_ids:
            block['block_id'] = block_id
            self.update_block(block)
            return False
        else:
            self.add_block(block_id, block)
            return True

    def add_parents(self, block_id, parents, recalculate_support = True):
        """Add parents to the block."""
        parents = self._dag_dict['blocks'][block_id]['parents'] + parents
        self._dag_dict['blocks'][block_id]['parents'] = list(set(parents))
        if recalculate_support:
            self._reset_parents_and_children()     
            
    def set_parents(self, block_id, parents):
        """Set parents of the block."""
        self._dag_dict['blocks'][block_id]['parents'] = parents
        self._reset_parents_and_children()

    def remove_block(self, block_id):
        """Remove block from the DAG. Does not remove the block file."""
        parents = self.parents_of(block_id)
        for child in self.children_of(block_id):
            self.add_parents(child, parents, recalculate_support = False)
            self._dag_dict['blocks'][child]['parents'].remove(block_id)
        del(self._dag_dict['blocks'][block_id])
        self._remove_redundant_parents()
        self._reset_parents_and_children()

    def block_filename(self, block_id):
        """Return block's filename as specified in the .dagpy file."""
        return self._dag_dict['blocks'][block_id]['file']

    def to_file(self, fpath):
        """Save the DAG to the .dagpy file."""
        return utils.dict_to_json_file(self._dag_dict, fpath)

    def update_blocks(self, blocks_meta):
        """Update blocks from the block_meta dicts."""
        for block_meta in blocks_meta:
             self.update_block(block_meta, recalculate_support = False)
        self._reset_parents_and_children()

    def update_block(self, block_meta, recalculate_support = True):
        """Update block from the block meta dict. Recalculates support (children, etc.) by default."""
        block_id = block_meta['block_id']
        for block_att in DAG.block_attributes:
            if block_att in block_meta:
                self._dag_dict['blocks'][block_id][block_att] = block_meta[block_att]
        if recalculate_support:
            self._reset_parents_and_children()


    @staticmethod
    def from_file(fpathname):
        """Create DAG object from the .dagpy file."""
        dag_dict = json.load(open(fpathname))
        return DAG(dag_dict)

    @staticmethod
    def empty(name):
        """Create an empty DAG object."""
        dag_dict = {'id': name, 'blocks': {}}
        return DAG(dag_dict)
