# ScruML
# uml_context_cli.py
# Team JJARS
import cmd
from typing import List
from typing import Optional
from typing import Tuple

from scruml import uml_filesystem_io
from scruml.uml_diagram import UMLDiagram


class __UMLShell(cmd.Cmd):
    """Simple CLI context for interacting with ScrUML"""

    intro: str = "Welcome to ScrUML.\nType in 'help' to receive a list of possible commands."
    prompt: str = "ScrUML> "
    __diagram: UMLDiagram = UMLDiagram()

    # ----------
    # Helper functions

    def __classify_identifier(self, ident: str) -> str:
        ident = ident.strip()

        if ident.startswith("[") and ident.endswith("]"):
            ident = ident[1:-1]
            # TODO, parse rest of relationship identifier: [ classA, classB, name ]
        # TODO, parse rest of class identifier: name
        # no spaces in class names,
        # no spaces in relationship names
        return ""

    def __parse_class_identifier(self, ident: str) -> str:
        return ""

    def __parse_relationship_identifier(
        self, ident: str
    ) -> Tuple[str, str, Optional[str]]:
        return ("", "", None)

    # ----------
    # "Add" functions

    def do_add(self, arg: str) -> None:
        """Usage: add <identifier>
Adds new class or relationship if one with that identifier does not already exist
For help with identifiers, type in 'help identifiers'"""
        # TODO, implement identifier classification, parsing, and dispatching to subcommand
        pass

    def __add_class(self, arg: str) -> None:
        """Adds new class if one with that name does not already exist"""
        if not self.__diagram.add_class(arg):
            print("Class '{}' already exists in the diagram".format(arg))
        else:
            print("Added class '{}'".format(arg))

    def __add_relationship(self, arg: str) -> None:
        """Adds new relationship if one with that identifier does not already exist"""
        pass

    # ----------
    # "Remove" functions

    def do_remove(self, arg: str) -> None:
        """Usage: remove <identifier>"""
        # TODO, implement identifier classification, parsing, and dispatching to subcommand
        pass

    def do_remove_class(self, arg: str) -> None:
        """Removes class if it exists"""
        if not self.__diagram.remove_class(arg):
            print("Class '{}' does not exist in the diagram".format(arg))
        else:
            print("Removed class '{}'".format(arg))

    def do_list_classes(self, arg: str) -> None:
        """Usage: list_classes
Lists all classes present in the current diagram"""
        class_names: List[str] = self.__diagram.get_all_class_names()
        if not class_names:
            print("The current diagram is empty")
        else:
            print("All classes in the current diagram:")
            print("\n".join(class_names))

    def do_rename_class(self, arg: str) -> None:
        """Usage: rename_class <class name> <new class name>
Changes the name of a class if it exists and the new name is not taken"""
        names: List[str] = arg.split()
        if names[0] not in self.__diagram.get_all_class_names():
            print("Class '{}' does not exist in the diagram".format(names[0]))
            pass
        elif names[1] in self.__diagram.get_all_class_names():
            print("Class '{}' already exists in the diagram".format(names[1]))
            pass
        self.__diagram.rename_class(names[0], names[1])
        print("Renamed class '{}' to '{}'".format(names[0], names[1]))

    def do_save_diagram(self, arg: str) -> None:
        """Usage: save_diagram <file name>
Saves the current UML diagram to a file"""
        if uml_filesystem_io.save_diagram(self.__diagram, arg):
            print("Diagram successfully saved to '{}'".format(arg))
        else:
            print("Failed to save diagram to '{}'")

    def do_load_diagram(self, arg: str) -> None:
        """Usage: load_diagram <file name>
Loads an existing UML diagram from a file"""
        print("Loading diagram from '{}'".format(arg))
        self.__diagram = uml_filesystem_io.load_diagram(arg)

    def do_exit(self, arg: str) -> bool:
        """Usage: exit
Exits ScrUML"""
        print("Thank you for using ScrUML. Goodbye!")
        return True


def activate() -> None:
    __UMLShell().cmdloop()
