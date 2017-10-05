## Specifications and conventions

#### Block files
Blocks are saved as iPy notebook files which are internally saved as JSON. Our only addition is in the notebook metadata (which iPython will not overwrite on notebook edits), where we save the block id and a list of variables which are passed on through the filter. We do not save any other data in the notebook file, because we use its last-change datetime as an indicator if it needs to be re-executed. If block names or other attributes where saved here as well, their changes would trigger the re-execution.

#### DAG file
DAG file is a JSON consisting of two parts: a list of blocks and project properties. Each block in the list has the following fields:
 - id
 - name – a name which the user sets, and by which it referes to this block (when specifying dependencies or executing blocks).
 - description – optional description of the block
 - last_executed – datetime of the last time the block was executed. This is compared to the last time the block file was changed, to determine if it needs to be re-executed.
 - dependencies – list of block ids
 
Other, optional fields include:
 - creator_user_id
 - creation_datetime
 - ...

#### Block delimiter cells


#### Cache files

#### Flow notebooks
