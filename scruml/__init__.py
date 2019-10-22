# ScrUML
# __init__.py
# Team JJARS
import sys
from typing import List

from scruml import uml_context_cli
from scruml import uml_context_gui


def main(argv: List[str] = sys.argv) -> None:
    """Act as primary entry point for the program."""
    if len(argv) == 1 or (len(argv) == 2 and argv[1] == "--gui"):
        # If no arguments were passed or "--gui" was specified, run in GUI mode
        uml_context_gui.activate()
    elif len(argv) == 2 and argv[1] == "--cli":
        # If "--cli" was specified, run in CLI mode
        uml_context_cli.activate()
    else:
        print("usage: scruml [--gui | --cli]\n")
        print("Options:")
        print("--gui\t: run ScrUML in graphical user interface mode")
        print("--cli\t: run ScrUML in command line interface mode")


# If this file was loaded explicitly, run main()
if __name__ == "__main__":
    main()
