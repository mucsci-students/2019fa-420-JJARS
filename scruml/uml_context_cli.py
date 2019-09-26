# ScruML
# uml_context_cli.py
# Team JJARS
import cmd

import uml_filesystem_io
from uml_diagram import UMLDiagram


class __UMLShell(cmd.Cmd):

    __diagram: UMLDiagram = UMLDiagram()

    def do_exit(self, arg: str) -> bool:
        print("Thank you for using ScrUML. Goodbye!")
        return True

    def do_add_class(self, arg: str) -> None:
        """add_class [class name]
      Adds new class if one with that name does not already exist"""
        if self.__diagram.add_class(arg):
            print("'{}' class already exists in the diagram".format(arg))
        else:
            print("Added class '{}'".format(arg))

    def do_remove_class(self, arg: str) -> None:
        """remove_class [class name]
      Removes class if it exists"""
        if self.__diagram.remove_class(arg):
            print("'{}' class does not exist in the diagram".format(arg))
        else:
            print("Removed class '{}'".format(arg))

    def do_list_classes(self, arg: str) -> None:
        """Lists all classes"""
        print("All classes in the current diagram:")
        class_names: List[str] = __diagram.get_all_class_names()
        print("\n".join(class_names))

    def do_rename_class(self, arg: str) -> None:
        """rename_class [class name] [new class name]
      Changes name of class if one of that name exists"""
        names: str = arg.split()
        __diagram.rename_class(names[0], names[1])
        print("changing " + names[0] + " to " + names[1])

    def do_save(self, arg: str) -> None:
        """Saves UML diagram"""
        if uml_filesystem_io.save_diagram(self.__diagram, arg):
            print("Diagram successfully saved to '{}'".format(arg))
        else:
            print("Failed to save diagram to '{}'")

    def do_load(self, arg: str) -> None:
        """load [filename]
      Loads existing UML diagram"""
        print("Loading diagram from '{}'".format(arg))
        __diagram = uml_filesystem_io.load_diagram(arg)


def activate() -> None:
    __UMLShell().cmdloop("ScrUML> ")
