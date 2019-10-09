# ScruML uml_context_cli.py Team JJARS
import cmd
import os
from typing import List
from typing import Optional
from typing import Tuple

import uml_filesystem_io
from uml_diagram import UMLDiagram


class __UMLShell(cmd.Cmd):
    """Simple CLI context for interacting with ScrUML"""

    intro: str = "Welcome to ScrUML.\nType in 'help' to receive a list of possible commands."
    doc_header: str = "Commands (type 'help <command>'):"
    misc_header: str = "Other topics (type 'help <topic>'):"
    prompt: str = "ScrUML> "
    __diagram: UMLDiagram = UMLDiagram()

    # ----------
    # Helper functions

    def __parse_class_identifier(self, ident: str) -> Optional[str]:
        """Returns valid class identifier on success, or None on failure
Valid class identifiers contain no whitespace and are not surrounded by brackets"""
        ident = ident.strip()
        if " " in ident:
            return None
        if ident.startswith("[") and ident.endswith("]"):
            return None
        return ident

    def __parse_relationship_identifier(
        self, ident: str
    ) -> Optional[Tuple[str, str, Optional[str]]]:
        """Returns valid relationship identifier on success, or None on failure
Valid relationship identifiers are surrounded by brackets, contain two valid class names
separated by a comma, and an optional relationship name (also comma separated)"""
        ident = ident.strip()

        # Check for start and end brackets and then shear them away
        if ident.startswith("[") and ident.endswith("]"):
            ident = ident[1:-1]
        else:
            return None

        # Split up the string into a list
        ident_list: List[str] = ident.split(",")

        # Make sure that there were enough values provided in the identifier
        if len(ident_list) <= 1 or len(ident_list) >= 4:
            return None

        # Pull out and validate the two class names that should be in the identifier
        class_A_name: Optional[str] = self.__parse_class_identifier(ident_list[0])
        class_B_name: Optional[str] = self.__parse_class_identifier(ident_list[1])
        if not class_A_name or not class_B_name:
            return None

        # If a relationship name was provided, pull it out and validate it too
        # (Relationship names follow the same rules as class names for simplicity)
        relationship_name: Optional[str] = None
        if len(ident_list) == 3:
            relationship_name = self.__parse_class_identifier(ident_list[2])
            if not relationship_name:
                return None

        return (str(class_A_name), str(class_B_name), relationship_name)

    def __parse_attribute_identifier(self, ident: str) -> Optional[Dict[str, str]]:
        """Returns valid attribute identifier on success, or None on failure
	Valid attribute identifier are surrounded by brackets, contain one valid
	class and one valid attribute identifier"""

        ident = ident.strip()
        #Check for start and end brackets
        if ident.startswith("[") and ident.endswith("]"):
                ident = ident[1:-1]
        else:
                return None	

    def __classify_identifier(self, ident: str) -> Optional[str]:
        """Returns a string identifying the kind of identifier that "ident" represents
Possible values: "class", "relationship", None"""
        if self.__parse_class_identifier(ident):
            return "class"
        elif self.__parse_relationship_identifier(ident):
            return "relationship"
        else:
            return None

    def __yes_or_no_prompt(self, question: str) -> bool:
        """Prompts the user with "question" and waits for a "y/n" answer """
        while "Waiting for valid reply":
            reply = str(input(question + " [y/n]: ")).lower().strip()
            if reply[:1] == "y":
                return True
            if reply[:1] == "n":
                return False
        assert (
            False
        ), "This is unreachable code. If you are reading this, you're in trouble, buddy."

    # ----------
    # "Help" commands

    def help_identifiers(self) -> None:
        """Prints helpful information about identifier formatting."""
        print(
            "Identifiers are the names that represent elements within your UML diagram.\n"
        )
        print("Valid identifier types: Classes, Relationships\n")
        print("Classes:")
        print("  Class identifiers consist of a single string with no whitespace.")
        print("  Class identifiers cannot start and end with an opening and")
        print("  closing bracket.")
        print("Examples:")
        print('  Valid: "MyClass", "--lispObject!", "class20-ab"')
        print('  Invalid: "[someclass]", "my class"\n')
        print("Relationships:")
        print("  Relationship identifiers consist of a bracketed list of")
        print("  2-3 valid class identifiers. The first two class identifiers")
        print("  represent the two classes that the relationship exists between.")
        print("  The third identifier represents the name of the relationship,")
        print("  though it is optional-- relationships can be unnamed.")
        print("Examples:")
        print('  Valid: "[ myclassA, myclassB ]", "[--object1,--object1,copy]"')
        print('  Invalid: "[class, my class]", "[[someclass], ]"')

    # ----------
    # "Add" command

    def do_add(self, arg: str) -> None:
        """Usage: add <identifier>
Adds new class or relationship if one with that identifier does not already exist
For help with identifiers, type in 'help identifiers'"""
        identifier_class: Optional[str] = self.__classify_identifier(arg)
        if identifier_class == "class":
            self.__add_class(arg)
        elif identifier_class == "relationship":
            self.__add_relationship(arg)
#	elif identifier_class == "attribute":
#	    self.__add_attribute(arg)
        else:
            print("Invalid argument provided.\n")
            print(self.do_add.__doc__)

    def __add_class(self, arg: str) -> None:
        """Adds new class if one with that name does not already exist"""
        arg = str(self.__parse_class_identifier(arg))
        if not self.__diagram.add_class(arg):
            print("Class '{}' already exists in the diagram".format(arg))
        else:
            print("Added class '{}'".format(arg))

    def __add_relationship(self, arg: str) -> None:
        """Adds new relationship if one with that identifier does not already exist"""
        print("Sorry! Relationships are coming in a future version of ScrUML.")

 #   def __add_attribute(self, arg: str) -> None:
#	"""Adds new attribute if one with that identifier does not already exist"""
	
    # ----------
    # "Remove" command

    def do_remove(self, arg: str) -> None:
        """Usage: remove <identifier>
Removes a class or relationship if one with that identifier exists in the diagram
For help with identifiers, type in 'help identifiers'"""
        identifier_class = self.__classify_identifier(arg)
        if identifier_class == "class":
            self.__remove_class(arg)
        elif identifier_class == "relationship":
            self.__remove_relationship(arg)
        else:
            print("Invalid argument provided.\n")
            print(self.do_add.__doc__)

    def complete_remove(
        self, text: str, line: str, begidx: str, endidx: str
    ) -> List[str]:
        """Return potential completions for the "remove" command"""
        return [
            name
            for name in self.__diagram.get_all_class_names()
            if name.startswith(text)
        ]

    def __remove_class(self, arg: str) -> None:
        """Removes class if it exists"""
        arg = str(self.__parse_class_identifier(arg))
        if not self.__diagram.remove_class(arg):
            print("Class '{}' does not exist in the diagram".format(arg))
        else:
            print("Removed class '{}'".format(arg))

    def __remove_relationship(self, arg: str) -> None:
        """Removes relationship if one with that identifier exists"""
        print("Sorry! Relationships are coming in a future version of ScrUML.")

    # ----------
    # "Rename" command

    def do_rename(self, arg: str) -> None:
        """Usage: rename <class name> <new class name>
Changes the name of a class if it exists and the new name is not taken
For help with identifiers, type in 'help identifiers"""
        names: List[str] = arg.split()
        if len(names) != 2:
            print("Please provide two valid class identifiers as arguments.\n")
            print(self.do_rename.__doc__)
            return
        identifiers: List[Optional[str]] = [
            self.__parse_class_identifier(names[0]),
            self.__parse_class_identifier(names[1]),
        ]
        if not identifiers[0] or not identifiers[1]:
            print("Please provide two valid class identifiers as arguments.\n")
            print(self.do_rename.__doc__)
            return
        if identifiers[0] not in self.__diagram.get_all_class_names():
            print("Class '{}' does not exist in the diagram".format(identifiers[0]))
            return
        elif identifiers[1] in self.__diagram.get_all_class_names():
            print(
                "Class with name '{}' already exists in the diagram".format(
                    identifiers[1]
                )
            )
            return
        self.__diagram.rename_class(str(identifiers[0]), str(identifiers[1]))
        print("Renamed class '{}' to '{}'".format(identifiers[0], identifiers[1]))

    def complete_rename(
        self, text: str, line: str, begidx: str, endidx: str
    ) -> List[str]:
        """Return potential completions for the "rename" command"""
        return [
            name
            for name in self.__diagram.get_all_class_names()
            if name.startswith(text)
        ]

    def __rename_class(self, arg: str) -> None:
        """TODO: Write me!"""
        pass

    def __rename_relationship(self, arg: str) -> None:
        """TODO: Write me!"""
        pass

    # ----------
    # Other functions

    def do_print(self, arg: str) -> None:
        """Usage: print
Prints all elements present in the current diagram"""
        class_names: List[str] = self.__diagram.get_all_class_names()
        if not class_names:
            print("The current diagram is empty")
        else:
            print("All classes in the current diagram:")
            print("\n".join(class_names))

    def do_save(self, arg: str) -> None:
        """Usage: save <file name>
Saves the current UML diagram to a file"""
        if arg.isspace() or not arg:
            print("Please provide a file name.\n")
            print(self.do_save.__doc__)
            return
        if uml_filesystem_io.save_diagram(self.__diagram, arg):
            print("Diagram successfully saved to '{}'".format(arg))
        else:
            print("Failed to save diagram to '{}'".format(arg))

    def do_load(self, arg: str) -> None:
        """Usage: load <file name>
Loads an existing UML diagram from a file"""
        if arg.isspace() or not arg:
            print("Please provide a file name.\n")
            print(self.do_load.__doc__)
            return
        if not os.path.isfile(arg):
            print("No file found at '{}'".format(arg))
            return
        if self.__diagram.get_all_class_names():
            print("Loading a diagram will overwrite the current diagram.")
            if not self.__yes_or_no_prompt("Continue?"):
                return
        print("Loading diagram from '{}'".format(arg))
        self.__diagram = uml_filesystem_io.load_diagram(arg)

    def do_exit(self, arg: str) -> bool:
        """Usage: exit
Exits ScrUML"""
        if self.__yes_or_no_prompt("Really exit ScrUML?"):
            print("Thank you for using ScrUML. Goodbye!")
            return True
        return False


def activate() -> None:
    __UMLShell().cmdloop()
