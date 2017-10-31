"""
This file implements the ``cea`` command line interface script. Basically, it uses the first argument passed to
it to look up a module to import in ``cli.config``, imports that and then calls the ``main`` function on that module.

The rest of the command line arguments are passed to the ``cea.config.Configuration`` object for processing.
"""

import sys
import os
import importlib
import ConfigParser
import cea.config


def main(config):
    cli_config = ConfigParser.SafeConfigParser()
    cli_config.read(os.path.join(os.path.dirname(__file__), 'cli.config'))

    # handle arguments
    args = sys.argv[1:]  # drop the script name from the arguments
    if not len(args):
        print_help(cli_config)
        sys.exit(1)
    script_name = args.pop(0)
    config.apply_command_line_args(args)

    module_path = cli_config.get('scripts', script_name)
    script_module = importlib.import_module(module_path)
    script_module.main(config)


def print_help(cli_config):
    """Print out the help message for the ``cea`` command line interface"""
    import textwrap
    print("usage: cea SCRIPT [OPTIONS]")
    print(textwrap.fill("SCRIPT can be one of: %s" % ', '.join(sorted(cli_config.options('scripts'))),
                        subsequent_indent='    ', break_on_hyphens=False))

if __name__ == '__main__':
    main(cea.config.Configuration())