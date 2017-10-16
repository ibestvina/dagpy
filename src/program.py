import api
import argparse
import os.path

this_filename = 'program.py'

parsing_errors = False

def is_valid_file(parser, arg):
    """Check if the file exists and return its path. Otherwise raise error."""
    if not arg: return arg
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg

def default_dagfile():
    """Get default DAG file path: the first *.dagpy file in the current folder."""
    global parsing_errors
    for file in os.listdir('./'):
        if file.endswith('.dagpy'):
            return file
    print('No default dagpy file found. Please specify it with [-d] flag.')
    parsing_errors = True



def run_default(args):
    """Running the script without any args."""
    print('Run {} -h for help.'.format(this_filename))

def run_create(args):
    """dagpy create"""
    print('Creating new project: {}'.format(args.name))
    api.new_project(args.name, args.run)

def run_view(args):
    """dagpy view"""
    print('Displaying DAG from {}'.format(args.dag_fpathname))
    api.display_dag(args.dag_fpathname, flow = args.blocks)

def run_exec(args):
    """dagpy execute"""
    if args.exec_all: print('Executing all blocks.\n\n')
    else: print('Executing blocks: {} and all their dependencies.\n\n'.format(', '.join(args.blocks)))
    api.execute_blocks(args.dag_fpathname, args.blocks, exec_all=args.exec_all)

def run_makeflow(args):
    """dagpy makeflow"""
    print('Making flow {} for blocks: {}'.format(args.flow_name, ', '.join(args.blocks)))
    api.create_flow(args.dag_fpathname, args.blocks, args.flow_name, run=args.run)

def run_submitflow(args):
    """dagpy submitflow"""
    print('Commiting flow from {}'.format(args.flow_notebook))
    api.update_from_flow(args.dag_fpathname, args.flow_notebook)

def run_blockrm(args):
    """dagpy remove"""
    print('Removing block {} from {}'.format(args.block, args.dag_fpathname))
    api.remove_block(args.dag_fpathname, args.block)


parser = argparse.ArgumentParser(prog='dagpy')
parser.set_defaults(func=run_default)
subparsers = parser.add_subparsers(title='DAGpy subcommands', description="This script provides you with the main DAGpy functionalities. \
    To find out more about each, run '{0} subcommand -h'. To start and run a new project, run '{0} create my_dagpy_project -r'".format(this_filename))

parser_create = subparsers.add_parser('create', help='Create new DAGpy project')
parser_create.add_argument('name', help='project name')
parser_create.add_argument('-r', '--run', dest='run', action='store_true', help='run the flow notebook of the newly created empty project',)
parser_create.set_defaults(func=run_create)

parser_view = subparsers.add_parser('view', help='Display the DAG')
parser_view.add_argument('blocks', nargs='*', help='blocks for which to highlight the flow (optional)', metavar='BLOCKS')
parser_view.add_argument('-d', '--dag', dest='dag_fpathname', help='DAG file (default: first .dagpy file in the current directory)', 
    default='', metavar='FILE', type=lambda x: is_valid_file(parser_exec, x))
parser_view.set_defaults(func=run_view)

parser_exec = subparsers.add_parser('execute', help='Execute DAG blocks', aliases=['exe'])
parser_exec.add_argument('blocks', nargs='*', help='blocks to execute', metavar='BLOCKS')
parser_exec.add_argument('-a', '--all', dest='exec_all', action='store_true', help='execute all blocks',)
parser_exec.add_argument('-d', '--dag', dest='dag_fpathname', help='DAG file', default='', metavar='FILE', type=lambda x: is_valid_file(parser_exec, x))
parser_exec.set_defaults(func=run_exec)

parser_makeflow = subparsers.add_parser('makeflow', help='Make a new flow', aliases=['mf'])
parser_makeflow.add_argument('blocks', nargs='+', help='blocks from which to create the flow', metavar='BLOCKS')
parser_makeflow.add_argument('-d', '--dag', dest='dag_fpathname', help='DAG file', default='', metavar='FILE', type=lambda x: is_valid_file(parser_exec, x))
parser_makeflow.add_argument('-n', '--name', dest='flow_name', help="name of the flow (default 'dagpy_flow')", default='dagpy_flow', metavar='NAME')
parser_makeflow.add_argument('-r', '--run', dest='run', action='store_true', help='run the flow notebook',)
parser_makeflow.set_defaults(func=run_makeflow)

parser_submitflow = subparsers.add_parser('submitflow', help='Submit the flow', aliases=['sf'])
parser_submitflow.add_argument('flow_notebook', help='flow notebook from which to update the DAG', type=lambda x: is_valid_file(parser_exec, x))
parser_submitflow.add_argument('-d', '--dag', dest='dag_fpathname', help='DAG file', default='', metavar='FILE', type=lambda x: is_valid_file(parser_exec, x))
parser_submitflow.set_defaults(func=run_submitflow)

parser_blockrm = subparsers.add_parser('remove', help='Remove block', aliases=['rm'])
parser_blockrm.add_argument('block', help='block to remove')
parser_blockrm.add_argument('-d', '--dag', dest='dag_fpathname', default='', help='DAG file', metavar='FILE', type=lambda x: is_valid_file(parser_exec, x))
parser_blockrm.add_argument('--removefile', dest='removefile', action='store_true', help='Remove the block file after removing the block from the DAG')
parser_blockrm.set_defaults(func=run_blockrm)


args = parser.parse_args()

if not hasattr(args, 'dag_fpathname') or not args.dag_fpathname:
    args.dag_fpathname = default_dagfile()

if parsing_errors:
    print('Errors occured')
else:
    args.func(args)
