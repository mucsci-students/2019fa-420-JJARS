# ScruML uml_context_cli.py Team JJARS
import cmd
import os
from argparse import ArgumentParser
from argparse import Namespace
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from scruml import uml_filesystem_io
from scruml import uml_utilities
from scruml.uml_diagram import UMLDiagram


# ----------
# __UMLShell class


class __UMLShell(cmd.Cmd):
    """Simple CLI context for interacting with ScrUML."""

    # --------------------
    # Static variables

    intro: str = "Welcome to ScrUML.\nType in 'help' to receive a list of possible commands."
    doc_header: str = "Commands (type 'help <command>'):"
    misc_header: str = "Other topics (type 'help <topic>'):"
    prompt: str = "ScrUML> "
    __diagram: UMLDiagram = UMLDiagram()

    # TODO: Standardize print strings, refactor dispatch functions

    def __yes_or_no_prompt(self, question: str) -> bool:
        """Prompts the user with "question" and waits for a "y/n" answer."""
        while "Waiting for valid reply":
            reply = str(input(question + " [y/n]: ")).lower().strip()
            if reply[:1] == "y":
                return True
            if reply[:1] == "n":
                return False
        assert (
            False
        ), "This is unreachable code. If you are reading this, you're in trouble, buddy."

    # --------------------
    # "Help" commands

    # ----------
    # emptyline

    def emptyline(self) -> bool:
        """Outputs a help line when the user does not enter a command."""
        print("Please enter a command.")
        print("Type in 'help' to receive a list of possible commands.")
        return False

    # ----------
    # help_identifiers

    def help_identifiers(self) -> None:
        """Prints helpful information about identifier formatting."""
        print(
            "Identifiers are the names that represent elements within your UML diagram.\n"
        )
        print("Valid identifier types: Classes, Relationships\n")
        print("Classes:")
        print(
            "  Class identifiers consist of a single string with no whitespace or quotes."
        )
        print("  Class identifiers cannot start and end with an opening and")
        print("  closing bracket.")
        print("Examples:")
        print('  Valid: "MyClass", "--lispObject!", "class20-ab"')
        print('  Invalid: "[someclass]", "my class", "class\'""\n')
        print("Relationships:")
        print("  Relationship identifiers consist of a bracketed list of")
        print("  2-3 valid class identifiers. The first two class identifiers")
        print("  represent the two classes that the relationship exists between.")
        print("  The third identifier represents the name of the relationship,")
        print("  though it is optional-- relationships can be unnamed.")
        print("Examples:")
        print('  Valid: "[myclassA,myclassB]", "[--object1,--object1,copy]"')
        print('  Invalid: "[class, my class]", "[[someclass], ]"')

    # ----------
    # help_parameters

    def help_parameters(self) -> None:
        """Prints helpful information about parameter list formatting."""
        print(
            "Parameter lists can be used to specify what arguments can be provided to a member function.\n"
        )
        print("Parameter lists:")
        print(
            "  Parameter lists consist of a bracketed list of one or more valid parameters."
        )
        print(
            "  Each parameter consists of a valid type name followed by a valid parameter name,"
        )
        print(
            "  separated by a single quote. Type names and parameter names cannot start and end with an"
        )
        print("  opening and closing bracket, and contain no whitespace or quotes.")
        print("Examples:")
        print("  Valid: \"[float'a,int'b,MyType'cx-var]\", \"[var'myStr,var'someVar]\"")
        print('  Invalid: "[ float;myvarone int myvartwo]", "[myVar, myVarB,]"')

    # ----------
    # "Add" command

    # ----------
    # do_add

    def do_add(self, arg: str) -> None:
        """Usage: add <identifier>
Adds new class or relationship if one with that identifier does not already exist
For help with identifiers, type in 'help identifiers'"""

        # Check the number of arguments
        args: List[str] = arg.split()
        if len(args) != 1:
            print(
                "Please provide a valid class or relationship identifier as an argument."
            )
            print(self.do_add.__doc__)
            return

        # Grab arguments
        identifier: str = args[0]

        # Classify what kind of identifier was provided
        identifier_class: Optional[str] = uml_utilities.classify_identifier(identifier)

        # Handle class identifiers
        if identifier_class == "class":
            class_id: Optional[str] = uml_utilities.parse_class_identifier(identifier)
            if class_id is not None:
                self.__add_class(arg)
                return

        # Handle relationship identifiers
        elif identifier_class == "relationship":
            rel_id: Optional[
                Tuple[str, str, Optional[str]]
            ] = uml_utilities.parse_relationship_identifier(identifier)
            if rel_id is not None:
                self.__add_relationship(rel_id)
                return

        # If we don't return before we get here, the user provided a bad argument
        print("Invalid argument provided.")
        print(self.do_add.__doc__)

    # ----------
    # __add_class

    def __add_class(self, class_id: str) -> None:
        """Adds new class if one with that name does not already exist"""
        if not self.__diagram.add_class(class_id):
            print("Class '{}' already exists in the diagram".format(class_id))
        else:
            print("Added class '{}'".format(class_id))

    # ----------
    # __add_relationship

    def __add_relationship(self, rel_id: Tuple[str, str, Optional[str]]) -> None:
        """Adds new relationship if one with that identifier does not already exist"""

        # Check whether both classes exist
        class_list: List[str] = self.__diagram.get_all_class_names()
        if rel_id[0] not in class_list:
            print("Class '{}' does not exist in the diagram".format(rel_id[0]))
            return
        if rel_id[1] not in class_list:
            print("Class '{}' does not exist in the diagram".format(rel_id[1]))
            return

        # Add the relationship to the diagram, checking for an error
        if not self.__diagram.add_relationship(rel_id[0], rel_id[1], rel_id[2]):
            print(
                "Relationship '{}' already exists in the diagram".format(
                    uml_utilities.stringify_relationship_identifier(
                        rel_id[0], rel_id[1], rel_id[2]
                    )
                )
            )
        else:
            print(
                "Added relationship '{}'".format(
                    uml_utilities.stringify_relationship_identifier(
                        rel_id[0], rel_id[1], rel_id[2]
                    )
                )
            )

    # --------------------
    # "Remove" command

    # ----------
    # do_remove

    def do_remove(self, arg: str) -> None:
        """Usage: remove <identifier>
Removes a class or relationship if one with that identifier exists in the diagram
For help with identifiers, type in 'help identifiers'"""

        # Check the number of arguments
        args: List[str] = arg.split()
        if len(args) != 1:
            print(
                "Please provide a valid class or relationship identifier as an argument."
            )
            print(self.do_remove.__doc__)
            return

        # Grab arguments
        identifier: str = args[0]

        # Classify what kind of identifier was provided
        identifier_class: Optional[str] = uml_utilities.classify_identifier(identifier)

        # Handle class identifiers
        if identifier_class == "class":
            class_id: Optional[str] = uml_utilities.parse_class_identifier(identifier)
            if class_id is not None:
                self.__remove_class(arg)
                return

        # Handle relationship identifiers
        elif identifier_class == "relationship":
            rel_id: Optional[
                Tuple[str, str, Optional[str]]
            ] = uml_utilities.parse_relationship_identifier(identifier)
            if rel_id is not None:
                self.__remove_relationship(rel_id)
                return

        # If we don't return before we get here, the user provided a bad argument
        print("Invalid argument provided.")
        print(self.do_remove.__doc__)

    # ----------
    # complete_remove

    def complete_remove(
        self, text: str, line: str, begidx: str, endidx: str
    ) -> List[str]:
        """Return potential completions for the "remove" command"""
        # TODO: Relationship completions
        return [
            name
            for name in self.__diagram.get_all_class_names()
            if name.startswith(text)
        ]

    # ----------
    # __remove_class

    def __remove_class(self, class_id: str) -> None:
        """Removes class if it exists"""
        if not self.__diagram.remove_class(class_id):
            print("Class '{}' does not exist in the diagram".format(class_id))
        else:
            print("Removed class '{}'".format(class_id))

    # ----------
    # __remove_relationship

    def __remove_relationship(self, rel_id: Tuple[str, str, Optional[str]]) -> None:
        """Removes relationship if one with that identifier exists"""

        # Check whether both classes exist
        class_list: List[str] = self.__diagram.get_all_class_names()
        if rel_id[0] not in class_list:
            print("Class '{}' does not exist in the diagram".format(rel_id[0]))
            return
        if rel_id[1] not in class_list:
            print("Class '{}' does not exist in the diagram".format(rel_id[1]))
            return

        # Remove the relationship from the diagram, checking for an error
        if not self.__diagram.remove_relationship(rel_id[0], rel_id[1], rel_id[2]):
            print(
                "Relationship '{}' does not exist in the diagram".format(
                    uml_utilities.stringify_relationship_identifier(
                        rel_id[0], rel_id[1], rel_id[2]
                    )
                )
            )
        else:
            print(
                "Relationship '{}' has been removed from the diagram".format(
                    uml_utilities.stringify_relationship_identifier(
                        rel_id[0], rel_id[1], rel_id[2]
                    )
                )
            )

    # --------------------
    # "Function" command

    # ----------
    # do_function

    def do_function(self, arg: str) -> None:
        """Usage: function [set|remove] <class name> <function name> [-v VISIBILITY] [-t TYPE] [-p PARAMETERS]
Adds, modifies, or removes a member function for the specified class
For help with formatting parameter lists, type in 'help parameters'"""

        # Check the number of arguments
        args: List[str] = arg.split()
        if len(args) < 3:
            print("Please provide a valid number of arguments.")
            print(self.do_function.__doc__)
            return

        # Grab arguments
        subcommand: str = args[0]
        class_name: str = args[1]
        func_name: str = args[2]

        # Parse the class ID and function name
        class_id: Optional[str] = uml_utilities.parse_class_identifier(class_name)
        func_id: Optional[str] = uml_utilities.parse_class_identifier(func_name)

        # Make sure that the class ID is valid
        if class_id is None:
            print(
                "Please provide a valid class name (no whitespace, quotes, or surrounding brackets)."
            )
            return

        # Make sure that the function ID is valid
        if func_id is None:
            print(
                "Please provide a valid function name (no whitespace, quotes, or surrounding brackets)."
            )
            return

        # Make sure that the class name is in the diagram
        if class_id not in self.__diagram.get_all_class_names():
            print("Class '{}' does not exist in the diagram".format(class_id))
            return

        # Handle set subcommand
        if subcommand == "set":

            # Set up argument parser for optional flags
            arg_parser: ArgumentParser = ArgumentParser(add_help=False, usage="")
            arg_parser.add_argument("-v", "--visibility")
            arg_parser.add_argument("-t", "--type")
            arg_parser.add_argument("-p", "--parameters")
            try:
                extra_args: Namespace = arg_parser.parse_args(args[3 : len(args)])
            except:
                print("Invalid argument provided.")
                print(self.do_function.__doc__)
                return

            # Grab and verify any optional flag values
            func_visibility: Optional[str] = ""
            func_type: Optional[str] = ""
            param_list: Optional[List[str]] = []
            if extra_args.visibility:
                func_visibility = uml_utilities.parse_class_identifier(
                    extra_args.visibility
                )
            if extra_args.type:
                func_type = uml_utilities.parse_class_identifier(extra_args.type)
            if extra_args.parameters:
                param_list = uml_utilities.parse_param_list(extra_args.parameters)
            if func_visibility is None or func_type is None or param_list is None:
                print(
                    "Please ensure all values provided are valid (no whitespace, quotes, or surrounding brackets)."
                )
                return

            # Dispatch
            self.__function_set(
                class_id, func_id, func_visibility, func_type, param_list
            )
            return

        # Handle remove subcommand
        if subcommand == "remove":
            self.__function_remove(class_id, func_id)
            return

        # If we don't return before we get here, the user provided a bad argument
        print("Invalid argument provided.")
        print(self.do_function.__doc__)

    # ----------
    # __function_set

    def __function_set(
        self,
        class_name: str,
        func_name: str,
        func_visibility: str,
        func_type: str,
        param_list: List[str],
    ) -> None:
        serialized_func: Tuple[str, str] = uml_utilities.serialize_function(
            func_visibility, func_type, func_name, param_list
        )
        self.__set_class_attribute(class_name, serialized_func[0], serialized_func[1])

    # ----------
    # __function_remove

    def __function_remove(self, class_name: str, func_name: str) -> None:
        self.__strip_class_attribute(class_name, f"[F:{func_name}]")

    # --------------------
    # "Variable" command

    # ----------
    # do_variable

    def do_variable(self, arg: str) -> None:
        """Usage: variable [set|remove] <class name> <variable name> [-v VISIBILITY] [-t TYPE]
Adds, modifies, or removes a member variable for the specified class"""

        # Check the number of arguments
        args: List[str] = arg.split()
        if len(args) < 3:
            print("Please provide a valid number of arguments.")
            print(self.do_variable.__doc__)
            return

        # Grab arguments
        subcommand: str = args[0]
        class_name: str = args[1]
        var_name: str = args[2]

        # Parse the class ID and variable name
        class_id: Optional[str] = uml_utilities.parse_class_identifier(class_name)
        var_id: Optional[str] = uml_utilities.parse_class_identifier(var_name)

        # Make sure that the class ID is valid
        if class_id is None:
            print(
                "Please provide a valid class name (no whitespace, quotes, or surrounding brackets)."
            )
            return

        # Make sure that the variable ID is valid
        if var_id is None:
            print(
                "Please provide a valid variable name (no whitespace, quotes, or surrounding brackets)."
            )
            return

        # Make sure that the class name is in the diagram
        if class_id not in self.__diagram.get_all_class_names():
            print("Class '{}' does not exist in the diagram".format(class_id))
            return

        # Handle set subcommand
        if subcommand == "set":

            # Set up argument parser for optional flags
            arg_parser: ArgumentParser = ArgumentParser(add_help=False, usage="")
            arg_parser.add_argument("-v", "--visibility")
            arg_parser.add_argument("-t", "--type")
            try:
                extra_args: Namespace = arg_parser.parse_args(args[3 : len(args)])
            except:
                print("Invalid argument provided.")
                print(self.do_function.__doc__)
                return

            # Grab and verify any optional flag values
            var_visibility: Optional[str] = ""
            var_type: Optional[str] = ""
            if extra_args.visibility:
                var_visibility = uml_utilities.parse_class_identifier(
                    extra_args.visibility
                )
            if extra_args.type:
                var_type = uml_utilities.parse_class_identifier(extra_args.type)
            if var_visibility is None or var_type is None:
                print(
                    "Please ensure all values provided are valid (no whitespace, quotes, or surrounding brackets)."
                )
                return

            # Dispatch
            self.__variable_set(class_id, var_id, var_visibility, var_type)
            return

        # Handle remove subcommand
        if subcommand == "remove":
            self.__variable_remove(class_id, var_id)
            return

        # If we don't return before we get here, the user provided a bad argument
        print("Invalid argument provided.")
        print(self.do_variable.__doc__)

    # ----------
    # __variable_set

    def __variable_set(
        self, class_name: str, var_name: str, var_visibility: str, var_type: str
    ) -> None:
        serialized_var: Tuple[str, str] = uml_utilities.serialize_variable(
            var_visibility, var_type, var_name
        )
        self.__set_class_attribute(class_name, serialized_var[0], serialized_var[1])

    # ----------
    # __variable_remove

    def __variable_remove(self, class_name: str, var_name: str) -> None:
        self.__strip_class_attribute(class_name, f"[V:{var_name}]")

    # --------------------
    # "Set" command

    # ----------
    # do_set

    def do_set(self, arg: str) -> None:
        """Usage: set <identifier> <attribute_name> <attribute_value>
Adds or modifies the attribute for the specified class
For help with identifiers, type in 'help identifiers'"""

        # Check the number of arguments
        args: List[str] = arg.split()
        if len(args) != 3:
            print("Please provide a valid number of arguments.")
            print(self.do_set.__doc__)
            return

        # Grab arguments
        identifier: str = args[0]
        attr_name: str = args[1]
        attr_value: str = args[2]

        # Classify what kind of identifier was provided
        identifier_class: Optional[str] = uml_utilities.classify_identifier(identifier)

        # Ensure attribute name is valid
        if not uml_utilities.parse_class_identifier(attr_name):
            print(
                "Please provide a valid attribute name (no whitespace, quotes, or surrounding brackets)."
            )
            return

        # Handle class identifiers
        if identifier_class == "class":
            class_id: Optional[str] = uml_utilities.parse_class_identifier(identifier)
            if class_id is not None:
                self.__set_class_attribute(class_id, attr_name, attr_value)
                return

        # Handle relationship identifiers
        elif identifier_class == "relationship":
            rel_id: Optional[
                Tuple[str, str, Optional[str]]
            ] = uml_utilities.parse_relationship_identifier(identifier)
            if rel_id is not None:
                self.__set_relationship_attribute(rel_id, attr_name, attr_value)
                return

        # If we don't return before we get here, the user provided a bad argument
        print("Invalid argument provided.")
        print(self.do_set.__doc__)

    # ----------
    # __set_class_attribute

    def __set_class_attribute(
        self, class_id: str, attr_name: str, attr_value: str
    ) -> None:
        """Adds or modifies the attribute with attr_name for the specified class"""
        if not self.__diagram.set_class_attribute(class_id, attr_name, attr_value):
            print("Class '{}' does not exist in the diagram".format(class_id))
        else:
            print(
                "Set attribute '{}' with value '{}' in class '{}'".format(
                    attr_name, attr_value, class_id
                )
            )

    # ----------
    # __set_relationship_attribute

    def __set_relationship_attribute(
        self, rel_id: Tuple[str, str, Optional[str]], attr_name: str, attr_value: str
    ) -> None:
        """Adds or modifies the attribute with attr_name for the specified relationship."""

        # Check whether both classes exist
        class_list: List[str] = self.__diagram.get_all_class_names()
        if rel_id[0] not in class_list:
            print("Class '{}' does not exist in the diagram".format(rel_id[0]))
            return
        if rel_id[1] not in class_list:
            print("Class '{}' does not exist in the diagram".format(rel_id[1]))
            return

        # Set the relationship's attribute, checking for an error
        if not self.__diagram.set_relationship_attribute(
            rel_id[0], rel_id[1], rel_id[2], attr_name, attr_value
        ):
            print(
                "Relationship {} does not exist in the diagram".format(
                    uml_utilities.stringify_relationship_identifier(
                        rel_id[0], rel_id[1], rel_id[2]
                    )
                )
            )
        else:
            print(
                "Set attribute '{}' with value '{}' in relationship '{}'".format(
                    attr_name,
                    attr_value,
                    uml_utilities.stringify_relationship_identifier(
                        rel_id[0], rel_id[1], rel_id[2]
                    ),
                )
            )

    # --------------------
    # "Strip" command

    # ----------
    # do_strip

    def do_strip(self, arg: str) -> None:
        """Usage strip <identifier> <attribute_name>
Removes the attribute for the specified class"""

        # Check the number of arguments
        args: List[str] = arg.split()
        if len(args) != 2:
            print("Please provide a valid number of arguments.")
            print(self.do_strip.__doc__)
            return

        # Grab arguments
        identifier: str = args[0]
        attr_name: str = args[1]

        # Classify what kind of identifier was provided
        identifier_class: Optional[str] = uml_utilities.classify_identifier(identifier)

        # Ensure attribute name is valid
        if not uml_utilities.parse_class_identifier(attr_name):
            print(
                "Please provide a valid attribute name (no whitespace, quotes, or surrounding brackets)."
            )
            return

        # Handle class identifiers
        if identifier_class == "class":
            class_id: Optional[str] = uml_utilities.parse_class_identifier(identifier)
            if class_id is not None:
                self.__strip_class_attribute(class_id, attr_name)
                return

        # Handle relationship identifiers
        elif identifier_class == "relationship":
            rel_id: Optional[
                Tuple[str, str, Optional[str]]
            ] = uml_utilities.parse_relationship_identifier(identifier)
            if rel_id is not None:
                self.__strip_relationship_attribute(rel_id, attr_name)
                return

        # If we don't return before we get here, the user provided a bad argument
        print("Invalid argument provided.")
        print(self.do_strip.__doc__)

    # ----------
    # __strip_class_attribute

    def __strip_class_attribute(self, class_id: str, attr_name: str) -> None:
        """Removes the attribute for the specified class"""
        if class_id not in self.__diagram.get_all_class_names():
            print("Class '{}' does not exist in the diagram".format(class_id))
            return
        if not self.__diagram.remove_class_attribute(class_id, attr_name):
            print(
                "Class '{}' does not have an attribute with name '{}'".format(
                    class_id, attr_name
                )
            )
        else:
            print("Removed attribute '{}' from class '{}'".format(attr_name, class_id))

    # ----------
    # __strip_relationship_attribute

    def __strip_relationship_attribute(
        self, rel_id: Tuple[str, str, Optional[str]], attr_name: str
    ) -> None:
        """Removes the attribute with attr_name for the specified relationship."""

        # Check whether both classes exist
        class_list: List[str] = self.__diagram.get_all_class_names()
        if rel_id[0] not in class_list:
            print("Class '{}' does not exist in the diagram".format(rel_id[0]))
            return
        if rel_id[1] not in class_list:
            print("Class '{}' does not exist in the diagram".format(rel_id[1]))
            return

        # Remove the relationship's attribute, checking for an error
        if not self.__diagram.remove_relationship_attribute(
            rel_id[0], rel_id[1], rel_id[2], attr_name
        ):
            print(
                "Relationship '{}' does not have an attribute with name '{}'".format(
                    uml_utilities.stringify_relationship_identifier(
                        rel_id[0], rel_id[1], rel_id[2]
                    ),
                    attr_name,
                )
            )
        else:
            print(
                "Removed attribute '{}' from relationship '{}'".format(
                    attr_name,
                    uml_utilities.stringify_relationship_identifier(
                        rel_id[0], rel_id[1], rel_id[2]
                    ),
                )
            )

    # --------------------
    # "Rename" command

    # ----------
    # do_rename

    def do_rename(self, arg: str) -> None:
        """Usage: rename <class name> <new class name>
Changes the name of a class if it exists and the new name is not taken
For help with identifiers, type in 'help identifiers"""

        # Check the number of arguments
        args: List[str] = arg.split()
        if len(args) != 2:
            print("Please provide a valid number of arguments.")
            print(self.do_rename.__doc__)
            return

        # Grab arguments
        old_class_name: str = args[0]
        new_class_name: str = args[1]

        # Parse the class IDs
        class_ids: List[Optional[str]] = [
            uml_utilities.parse_class_identifier(old_class_name),
            uml_utilities.parse_class_identifier(new_class_name),
        ]

        # Make sure that the class ids are valid
        if not class_ids[0] or not class_ids[1]:
            print("Please provide two valid class class_ids as arguments.")
            print(self.do_rename.__doc__)
            return

        # Make sure that the old class name is in the diagram
        if class_ids[0] not in self.__diagram.get_all_class_names():
            print("Class '{}' does not exist in the diagram".format(class_ids[0]))
            return

        # Rename the class, checking for an error
        if not self.__diagram.rename_class(str(class_ids[0]), str(class_ids[1])):
            print(
                "Class with name '{}' already exists in the diagram".format(
                    class_ids[1]
                )
            )
            return
        else:
            print("Renamed class '{}' to '{}'".format(class_ids[0], class_ids[1]))

        # If we don't return before we get here, the user provided a bad argument
        print("Invalid argument provided.")
        print(self.do_rename.__doc__)

    # ----------
    # complete_rename

    def complete_rename(
        self, text: str, line: str, begidx: str, endidx: str
    ) -> List[str]:
        """Return potential completions for the "rename" command"""
        # TODO: Split arguments
        return [
            name
            for name in self.__diagram.get_all_class_names()
            if name.startswith(text)
        ]

    # --------------------
    # Other functions

    # ----------
    # do_print

    def do_print(self, arg: str) -> None:
        """Usage: print
Prints all elements present in the current diagram"""

        class_names: List[str] = self.__diagram.get_all_class_names()

        if not class_names:
            print("The current diagram is empty.")
            return

        print("All classes in the current diagram:")

        for class_name in class_names:

            print(" " + class_name + ":")

            attributes: Optional[Dict[str, str]] = self.__diagram.get_class_attributes(
                class_name
            )

            if attributes is None:
                raise Exception(
                    "Fatal: Attributes entry for class '{}' not found.".format(
                        class_name
                    )
                )

            if attributes == {}:
                print("   No attributes")

            for attribute_name, attribute_value in attributes.items():
                print("   {} = {}".format(attribute_name, attribute_value))

        relationship_pairs: List[
            Tuple[str, str]
        ] = self.__diagram.get_all_relationship_pairs()

        print("All relationships in the current diagram:")

        if not relationship_pairs:
            print(" No relationships")

        for relationship_pair in relationship_pairs:

            relationships: Optional[
                Dict[Optional[str], Dict[str, str]]
            ] = self.__diagram.get_relationships_between(
                relationship_pair[0], relationship_pair[1]
            )

            if relationships is None:
                raise Exception(
                    "Fatal: Relationships entry for class pair '[{},{}]'".format(
                        relationship_pair[0], relationship_pair[1]
                    )
                )

            for relationship_name in relationships:

                print(
                    " {} <-> {}{}:".format(
                        relationship_pair[0],
                        relationship_pair[1],
                        ""
                        if relationship_name is None
                        else " (" + relationship_name + ")",
                    )
                )

                relationship_attributes: Optional[
                    Dict[str, str]
                ] = self.__diagram.get_relationship_attributes(
                    relationship_pair[0], relationship_pair[1], relationship_name
                )
                if relationship_attributes is None or relationship_attributes == {}:
                    print("   No attributes")
                else:

                    for (
                        rel_attribute_name,
                        rel_attribute_value,
                    ) in relationship_attributes.items():
                        print(
                            "   {} = {}".format(rel_attribute_name, rel_attribute_value)
                        )

    # ----------
    # do_save

    def do_save(self, arg: str) -> None:
        """Usage: save <file name>
Saves the current UML diagram to a file"""
        if arg.isspace() or not arg:
            print("Please provide a file name.")
            print(self.do_save.__doc__)
            return
        if uml_filesystem_io.save_diagram(self.__diagram, arg):
            print("Diagram successfully saved to '{}'".format(arg))
        else:
            print("Failed to save diagram to '{}'".format(arg))

    # ----------
    # do_load

    def do_load(self, arg: str) -> None:
        """Usage: load <file name>
Loads an existing UML diagram from a file"""
        if arg.isspace() or not arg:
            print("Please provide a file name.")
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

    # ----------
    # do_exit

    def do_exit(self, arg: str) -> bool:
        """Usage: exit
Exits ScrUML"""
        if self.__yes_or_no_prompt("Really exit ScrUML?"):
            print("Thank you for using ScrUML. Goodbye!")
            return True
        return False


# ----------
# activate


def activate() -> None:
    """Activates the CLI context."""
    __UMLShell().cmdloop()
