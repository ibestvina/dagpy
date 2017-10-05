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
 - **Filter** — special block which filters and caches out the data passed from one block to another. Filter can be turned off, in which case the whole interpreter session state is passed. Eventually, users would be able to choose which filtered elements are cached (see Milestones).
 - **DAG** — directed acyclic graph of blocks, where a connection A <- B denotes a dependency of block B to block A.
 
Each block is saved as ipynb file. Apart from those, project consists of a DAG file, where DAG and other project metadata is saved, and cache files produced by filters. Users can choose whether to only save the most recent versions of cached objects (presumably because previous versions are managed by VC systems), or to save the _n_ most recent ones.


## Mechanics
This section describes the current state of the DAGpy mechanics. It will be updated as the project develops and the mechanics change (as described in the Milestones).

DAGpy consists of two subsystems: DAG manager and DAG executor. **DAG manager** deals with the block creation and editing, DAG parsing and editing, DAG change tracking (i.e. answering the question "Which blocks should be re-executed?"), and cache files managing. DAG manager also serves the notebooks built from some block and its dependencies to users. **DAG executor** executes the DAG or its subset (on request, schedule or trigger), automatically paralellizing DAG branches when possible, and managing block communication (first trivially through files, later through MPI).

Common work flow for a small data sci team is as follows. Suppose Alice and Bob are working on a data analysis job for a telecom client, who provided some user data, and wants to know how these users are clustered. First, Alice creates three blocks: A1 — data loading, B1 — data cleaning, and C1 — some simple description of the data (user counts, column-wise statistics, etc.). Current DAG state is [A1 <- B1 <- C1].

Bob now wants to visualize how much traffic users generate through time. He selects the B1 block and the system serves him a notebook consisting of blocks A1 and B1, with the addition of the cached data loading after the B1, so Bob does not need to re-run the entire notebook — only this last cell. Bob now aggregates the user traffic, creating the block C2. He inserts a block delimiter into the notebook specifying the filter and the following block dependencies (suppose he chose C2), and continues writing the visualization cells, building the block D1. When he finishes and commits the notebook to the system, it automatically detects the two newly created blocks and adds them to the DAG. By default, their dependencies are linear after the block from which the user started, so DAG is now defined as [A1 <- B1 <- [C1, C2 <- D2]] (we denote DAG branching as a list of branches).

Next, Alice wants to cluster users based on their traffic relative to the overall user traffic for some period. She selects both blocks B1 and C2, and using their (cached) outputs creates new blocks: E1 — data merging, and F1 — user clustering. During their work, the client notifies them that they should filter out international calls, and base their analysis on local traffic only. They can now simply add this filtering to B1, and re-execute the DAG starting from B1.

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
