# ScruML
# uml_context_cli.py
# Team JJARS
import cmd
from typing import List

from scruml import uml_filesystem_io
from scruml.uml_diagram import UMLDiagram


class __UMLShell(cmd.Cmd):
    """Simple CLI context for interacting with ScrUML"""

    intro: str = "Welcome to ScrUML.\nType in 'help' to receive a list of possible commands."
    prompt: str = "ScrUML> "
    __diagram: UMLDiagram = UMLDiagram()

    def do_exit(self, arg: str) -> bool:
        """Usage: exit
Exits ScrUML"""
        print("Thank you for using ScrUML. Goodbye!")
        return True

    def do_add_class(self, arg: str) -> None:
        """Usage: add_class <class name>
Adds new class if one with that name does not already exist"""
        if not self.__diagram.add_class(arg):
            print("Class '{}' already exists in the diagram".format(arg))
        else:
            print("Added class '{}'".format(arg))

    def do_remove_class(self, arg: str) -> None:
        """Usage: remove_class <class name>
Removes class if it exists"""
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


def activate() -> None:
    __UMLShell().cmdloop()
