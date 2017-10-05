## Specifications and conventions

#### Block files
Blocks are saved as iPy notebook files which are internally saved as JSON. Our only addition is in the notebook metadata (which iPython will not overwrite on notebook edits), where we save the block id and a list of variables which are passed on through the filter. We do not save any other data in the notebook file, because we use its last-change datetime as an indicator if it needs to be re-executed. If block names or other attributes where saved here as well, their changes would trigger the re-execution.

#### DAG file

### Block delimiter cells

#### Cache files

#### Flow notebooks
