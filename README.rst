DAGpy
=====

DAGpy is a data science collaboration tool based on iPython notebooks
enabling data science teams to: - easily collaborate by branching out of
others' notebooks - minimize code duplication - give a clean overview of
the project - cache intermediate outputs so team members can use them
without re-evaluation - automate the process of code execution upon data
changes or on schedule - provide a clean interface to the data
visualization dashboard designers and developers

DAGpy manages a DAG (directed acyclic graph) of blocks of code, with
each block being a sequence of iPython notebook cells, together with
their outputs. It is designed to work seamlessly with popular VC systems
like git and can be run locally or as a server application.

To learn more about DAGpy read the `Project
overview <docs/project_overview.md>`__. This is a work in progress. PIP
package (version 0.1) coming soon!

Author: Ivan Bestvina

Example project
---------------

To play around with the example project, you can: - view the project
DAG: ``python program.py view`` - run all the blocks:
``python program.py execute -a`` - add blocks through flows (with block
B as a parent) and run them automatically:
``python program.py makeflow B -r`` - commit the changes:
``python program.py submitflow dagpy_flow.ipynb`` - explore other DAGpy
options with ``python program.py -h``

Please note that notebook execution time includes a significant overhead
of over a second, because a kernel must be started for each one. In
future, we plan on adding support for non-notebook plane python blocks.
These would also be edited through a flow notebook view, but would be
saved as .py scripts, and executed without noticable overhead.

Dependencies: - python 3 - jupyter - dill - networkx, matplotlib (for
DAG view)
