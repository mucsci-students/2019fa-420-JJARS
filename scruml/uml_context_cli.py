# ScruML
# uml_context_cli.py
# Team JJARS
import cmd

import uml_filesystem_io
from uml_diagram import UMLDiagram


class __UMLShell(cmd.Cmd):

    __diagram: UMLDiagram = UMLDiagram()

    def do_exit(self, arg: str):
        print("Exited")
        return True

    def do_add_class(self, arg: str):
        """add_class [class name]
      Adds new class if one with that name does not already exist"""
        add_class_name: str = self.__diagram.add_class(arg)
        if add_class_name == None:
            print("'{}' class already exists".format(arg))
        else:
            print("Added '{}' class".format(arg))

    def do_remove_class(self, arg: str):
        """remove_class [class name]
      Removes class if it exists"""
        remove_class_name: str = __diagram.remove_class(arg)
        if remove_class_name == None:
            print("'{}' class does not exist".format(arg))
        else:
            print("Removed '{}' class".format(arg))

    def do_list_classes(self, arg: str):
        """Lists all classes"""
        print("Listing all classes:")
        class_names: List[str] = __diagram.get_all_class_names()
        print("\n".join(class_names))

    def do_rename_class(self, arg: str):
        """rename_class [class name] [new class name]
      Changes name of class if one of that name exists"""
        names: str = arg.split()
        __diagram.rename_class(names[0], names[1])
        print("changing " + names[0] + " to " + names[1])

    def do_save(self, arg: str):
        """Saves UML diagram"""

    def do_load(self, arg: str):
        """load [filename]
      Loads existing UML diagram"""
        print("Loading '{}'".format(arg))


def activate():
    __UMLShell().cmdloop("ScrUML> ")
