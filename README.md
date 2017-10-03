# DAGpy

DAGpy is a data science collaboration tool based on iPython notebooks enabling data science teams to:
 - easily collaborate by branching out of others' notebooks
 - minimize code duplication
 - give a clean overview of the project
 - cache intermediate outputs so team members can use them without evaluation
 - automate the process of code execution upon data changes or on schedule
 - provide a clean interface to the data visualization dashboard designers and developers

DAGpy manages a DAG (directed acyclic graph) of blocks of code, with each block being a sequence of iPython notebook cells, together with their outputs. It is designed to work seamlessly with popular VC systems like git and can be run locally or as a server application.

To learn more about DAGpy read the [Project overview](doc/project_overview.md).
