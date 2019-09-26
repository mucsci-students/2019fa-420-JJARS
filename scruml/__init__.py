# ScrUML
# __init__.py
# Team JJARS

import scruml.uml_context_cli


def main() -> None:
    """Act as primary entry point for the program."""
    uml_context_cli.activate()


# If this file was loaded explicitly, run main()
if __name__ == "__main__":
    main()
