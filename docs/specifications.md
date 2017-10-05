## Specifications and conventions

### Block files
Blocks are saved as iPy notebook files which are internally saved as JSON. Our only addition is in the notebook metadata (which iPython will not overwrite on notebook edits), where we save the block id and a list of variables which are passed on through the filter. We do not save any other data in the notebook file, because we use its last-change datetime as an indicator if it needs to be re-executed. If block names or other attributes where saved here as well, their changes would trigger the re-execution.

### DAG file
DAG file is a JSON consisting of two parts: a list of blocks and project properties. Each block in the list has the following fields:
 - id
 - name – a name which the user sets, and by which it refers to this block (when specifying dependencies or executing blocks). Block names are not case-sensitive and must be unique.
 - description – optional description of the block
 - last_executed – datetime of the last time the block was executed. This is compared to the last time the block file was changed, to determine if it needs to be re-executed.
 - dependencies – list of block ids
 - blockfile – full path to the ipynb file holding this block
 
Other, optional fields include:
 - creator_user_id
 - creation_datetime
 - ...
 
 If the system detects (for example, upon DAG execution) that a certain file is missing, it reports it back to the user. User can, at any time, import new ipynb files to the project, filepaths of which the system then updates in the DAG file, identifying them by the id in the block file. This way, if the project folder structure changes, users can simply re-import their blockfiles to update the DAG file.
 
 As already mentioned, DAG file also holds the project metadata. This includes:
 - name – name of the project
 - cache_dir – path to the cache files
 - ...

### Block delimiter cells
When users request some flow to change its blocks or add new blocks to it, they are presented with the iPy notebook built from the blocks which are included in that flow. These blocks are delimited by special cells which are both the visual guide to the user and a reference to us, so it is possible for the system to track changes made to the blocks. To make them as user-friendly as possible, we decided to use markdown cells for this purpose, and to save our internal data (mainly the block ids) into their metadata. As we would like these blocks to be as flexible as possible, we set out the following rules for the block attribute specification through markdown delimiter cells:
 - Each attribute name is written as one line of markdown heading text, using any heading level. In other words, each attribute name is a line which starts with '\#' sign, and all the other '\#' signs are ignored. Attribute names are not case-sensitive.
 - Attribute value is specified in the following lines, until a new attribute name is introduced, or until the end of the cell.
 - If the attribute value cannot hold newlines or whitespaces, these are ignored.
 - List attribute values (such as block dependencies) can be delimited with commas, whitespaces and new lines.

### Cache files
Cache files hold raw binaries of python objects serialized using the Dill library. Their naming convention is <block_id>\_<var_name>.dill.

### Flow notebooks
Flow notebooks are built by concatenating blocks, without their ipynb metadata, delimited by the delimiter blocks described earlier. DAG subgraph from which the flow notebooks is built is linearized in a BFS fashion.
