# ScrUML
# __init__.py
# Team JJARS
import sys
from typing import List

from argparse import ArgumentParser
from argparse import Namespace

from scruml import uml_context_cli
from scruml import uml_context_gui


# ----------
# main

def main(argv: List[str] = sys.argv) -> None:
    """Act as primary entry point for the program."""

    arg_parser: ArgumentParser = ArgumentParser()

    arg_parser.add_argument("--cli", action='store_true', help="run ScrUML in command line interface mode")
    arg_parser.add_argument("--gui", action='store_true', help="run ScrUML in graphical user interface mode (default behavior)")
    arg_parser.add_argument("--debug", action='store_true', help="enable the developer console (GUI only)")

    args: Namespace = arg_parser.parse_args()

    if args.cli:
        uml_context_cli.activate()
        return

    uml_context_gui.activate(args.debug)

    # if len(argv) == 1 or (len(argv) in range(2,4) and argv[1] == "--gui"):
    #     # If no arguments were passed or "--gui" was specified, run in GUI mode
    #     uml_context_gui.activate((len(argv) == 3 and argv[2] == "--debug" or argv[1] == "--debug"))
    # elif len(argv) == 2 and argv[1] == "--cli":
    #     # If "--cli" was specified, run in CLI mode
    #     uml_context_cli.activate()
    # else:
    #     print("usage: scruml [--gui | --cli] [--debug]\n")
    #     print("Options:")
    #     print("--gui\t: run ScrUML in graphical user interface mode")
    #     print("--cli\t: run ScrUML in command line interface mode")
    #     print("--debug\t: run ScrUML with debugging enabled (GUI only)")


# If this file was loaded explicitly, run main()
if __name__ == "__main__":
    main()
