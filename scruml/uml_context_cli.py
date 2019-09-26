# ScruML
# uml_context_cli.py
# Team JJARS
import cmd
from typing import List

from scruml import uml_filesystem_io
from scruml.uml_diagram import UMLDiagram


class __UMLShell(cmd.Cmd):

    __diagram: UMLDiagram = UMLDiagram()

    def do_exit(self, arg: str) -> bool:
        print("Thank you for using ScrUML. Goodbye!")
        return True

    def help_commands(self) -> None:
        print("Possible commands:")
        print("add_class [class name]")
        print("remove_class [class name]")
        print("list_classes")
        print("rename_class [old class name] [new class name]")
        print("save_diagram [file path]")
        print("load_diagram [file path]")

    def do_add_class(self, arg: str) -> None:
        """add_class [class name]
      Adds new class if one with that name does not already exist"""
        if not self.__diagram.add_class(arg):
            print("'{}' class already exists in the diagram".format(arg))
        else:
            print("Added class '{}'".format(arg))

    def do_remove_class(self, arg: str) -> None:
        """remove_class [class name]
      Removes class if it exists"""
        if not self.__diagram.remove_class(arg):
            print("'{}' class does not exist in the diagram".format(arg))
        else:
            print("Removed class '{}'".format(arg))

    def do_list_classes(self, arg: str) -> None:
        """list_classes
      Lists all classes"""
        print("All classes in the current diagram:")
        class_names: List[str] = self.__diagram.get_all_class_names()
        print("\n".join(class_names))

    def do_rename_class(self, arg: str) -> None:
        """rename_class [old class name] [new class name]
      Changes name of class if one of that name exists"""
        names: List[str] = arg.split()
        self.__diagram.rename_class(names[0], names[1])
        print("changing " + names[0] + " to " + names[1])

    def do_save_diagram(self, arg: str) -> None:
        """save_diagram [filename]
      Saves UML diagram"""
        if uml_filesystem_io.save_diagram(self.__diagram, arg):
            print("Diagram successfully saved to '{}'".format(arg))
        else:
            print("Failed to save diagram to '{}'")

    def do_load_diagram(self, arg: str) -> None:
        """load_diagram [filename]
      Loads existing UML diagram"""
        print("Loading diagram from '{}'".format(arg))
        self.__diagram = uml_filesystem_io.load_diagram(arg)


def activate() -> None:
    print("Welcome to ScrUML.")
    print(" Type in 'help commands' to receive a list of possible commands.")
    __UMLShell().cmdloop()
