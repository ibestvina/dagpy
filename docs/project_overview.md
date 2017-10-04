# DAGpy
Small data science teams frequently utilize the iPython notebooks as their main data exploration tool, which often results in large amounts of code duplication between team members during all stages of the process: data loading, cleaning, transforming, etc. This code is prone to errors which are difficult to detect, is often extremely time-consuming to execute, and needs regular changes whenever the client provides additional domain information. Using the already written load/clean/transform code rarely happens, as team members work in isolated environments. 

Because of these drawbacks to the common workflow, we propose an iPython notebook extension, which draws inspiration from both VC systems like git, and flow/pipeline datasci tools like AzureML. Our main goals are:
 - Simplify the usage of the preexisting code fragments, thus avoiding code duplication.
 - Simplify the exploration of side-ideas, branching out from preexisting analysis, and reduce the time needed for such exploration to start, caching the previous results
 - Automate the process of notebook execution/update either when data changes or on a predefined schedule.
 - Make executions faster by merging and automatically parallelizing parts of the flows when possible


## Main components
To understand how we plan on solving these issues, we first must explain what the underlying system would look like, and how the user will interact with it.
 - **Block** — sequence of iPython notebook cells of any type, together with their outputs.
 - **Filter** — special block wich filters and caches out the data passed from one block to another. Filter can be turned off, in which case the whole interpreter session state is passed. Eventually, users would be able to choose which filtered elements are cached (see Milestones).
 - **DAG** — directed acyclic graph of blocks, where a connection A <- B denotes a dependency of block B to block A.
 
Each block is saved as ipynb file. Apart from those, project consists of a DAG file, where DAG and other project metadata is saved, and cache files produced by filters. Users can choose whether to only save the most recent versions od cache files (presumably because previous versions are managed by VC systems), or to save the _n_ most recent ones.


## Mechanics


## Milestones
1. Basic DAG executor and DAG manager functionality
    * add blocks
    * edit blocks
    * notebook view of the block and its dependencies
    * block update on notebook change
    * execute all blocks
    * update blocks affected by block changes 
    
    During this phase, parallelization will be implemented trivially by running blocks as independent notebooks using the nbconverter. Because of this, blocks will communicate through pickled object files (implemented with Dill library). Later, this will be solved using the Ipyparallel library with MPI, reducing the overhead and enabling us to communicate between blocks in memory.
 
2. DAG execution scheduling and trigger mechanics, DAG visualization

3. Parallelization based on Ipyparallel with MPI

4. DAG interaction GUI
