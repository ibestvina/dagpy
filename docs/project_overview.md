# DAGpy
Small data science teams frequently utilize the iPython notebooks as their main data exploration tool, which often results in large amounts of code duplication between team members during all stages of the process: data loading, cleaning, transforming, etc. This code is prone to errors which are difficult to detect, is often extremely time-consuming to execute, and needs regular changes whenever the client provides additional domain information. Using the already written load/clean/transform code rarely happens, as team members work in isolated environments. 

Because of these drawbacks to the common workflow, we propose an iPython notebook extension, which draws inspiration from both VC systems like git, and flow/pipeline datasci tools like AzureML. Our main goals are:
 - Simplify the usage of the preexisting code fragments, thus avoiding code duplication.
 - Simplify the exploration of side-ideas, branching out from preexisting analysis, and reduce the time needed for such exploration to start, caching the previous results
 - Automate the process of notebook execution/update either when data changes or on a predefined schedule.
 - Make executions faster by merging and automatically parallelizing parts of the flows when possible


## Main components
To understand how we plan on solving these issues, we first must explain what the underlying system would look like, and how the user will interact with it.
 - **Block** —
 - **DAG** — 

## Mechanics
