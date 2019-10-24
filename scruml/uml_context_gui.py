# ScrUML
# uml_context_gui.py
# Team JJARS
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import List
from typing import Union

import pkg_resources
import webview

from os import path

from scruml import uml_filesystem_io
from scruml.uml_diagram import UMLDiagram


# ----------
# __API

class __API:
    """Provides an API to the JavaScript running in the GUI window.
Can be called from the JavaScript as such: pywebview.api.FUNCTIONNAME( ... )"""

    # ----------
    # Static variables

    __diagram: UMLDiagram = UMLDiagram()

    # ----------
    # Diagram information functions

    # ----------
    # getAllClassses

    def getAllClasses(self, params: str) -> Dict[str, Dict[str, str]]:
        """Returns a dictionary containing all class information in the diagram.
Structure: dictionary[className][attributeName] == attributeValue"""

        response: Dict[str, Dict[str, str]] = {}

        # Populate response dictionary with classes
        for class_name in self.__diagram.get_all_class_names():

            class_attributes: Optional[Dict[str, str]] = self.__diagram.get_class_attributes(class_name)

            if class_attributes is not None:
                response[class_name] = class_attributes
            else:
                raise Exception("Class not found in diagram: " + class_name)

        return response

    # ----------
    # getAllRelationships

    def getAllRelationships(self, params: str) -> Dict[str, Dict[str, str]]:
        """Returns a dictionary containing all relationship infromation in the diagram.
Structure: dictionary[classPair][relationshipName][attributeName] == attributeValue"""

        response: Dict[str, Dict[str, str]] = {}

        # Populate response dictionary with relationships
        for class_pair in self.__diagram.get_all_relationship_pairs():

            relationships: Optional[Dict[
                Optional[str], Dict[str, str]
            ]] = self.__diagram.get_relationships_between(class_pair[0], class_pair[1])

            if relationships is not None:
                for relationship_name in relationships:

                    relationship_id: str = ("["
                                            + class_pair[0]
                                            + ","
                                            + class_pair[1]
                                            + (("," + relationship_name) if relationship_name else "")
                                            + "]")

                    response[relationship_id] = {}

                    # TODO: Relationship Attributes, Sprint 3

            else:
                raise Exception("Class pair not found in diagram: [" + class_pair[0] + "," + class_pair[1] + "]")

        return response

    # ----------
    # __parse_class_identifier

    def __parse_class_identifier(self, ident: str) -> Optional[str]:
        """Returns valid class identifier on success, or None on failure
Valid class identifiers contain no whitespace and are not surrounded by brackets"""
        ident = ident.strip()
        if " " in ident:
            return None
        if '"' in ident:
            return None
        if "'" in ident:
            return None
        if ident.startswith("[") and ident.endswith("]"):
            return None
        return ident

    # ----------
    # __parse_relationship_identifier

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

    # ----------
    # Diagram file functions

    # ----------
    # newDiagramFile

    def newDiagramFile(self, params: str) -> None:
        """Creates a new, blank diagram."""
        self.__diagram = UMLDiagram()

    # ----------
    # loadDiagramFile

    def loadDiagramFile(self, params: str) -> None:
        """Opens a file selector dialog and loads the selected diagram file."""

        # Define supported file types
        file_types: Tuple[str, str] = (
            "ScrUML Files (*.scruml;*.yaml)",
            "All Filles (*.*)",
        )

        # Open load file dialog
        dialog_result: Union[Tuple[str],
                             str,
                             None] = webview.windows[0].create_file_dialog(
            webview.OPEN_DIALOG, file_types=file_types
        )
        file_path: str = ""

        # Different platforms do different things here, why????
        if not dialog_result:
            return
        elif isinstance(dialog_result, tuple):
            file_path = dialog_result[0]
        elif isinstance(dialog_result, str):
            file_path = dialog_result

        # Make sure the user selected a file
        if len(file_path) == 0:
            return

        # Load the new diagram file
        self.__diagram = uml_filesystem_io.load_diagram(file_path)

    # ----------
    # saveDiagramFile

    def saveDiagramFile(self, params: str) -> str:
        """Opens a file save dialog and saves to the specified diagram file."""

        file_types: Tuple[str, str] = (
            "ScrUML Files (*.scruml;*.yaml)",
            "All Filles (*.*)",
        )

        # Get OS-specific home path
        home_path: str = path.abspath("~/")

        # Open save file dialog
        dialog_result: Union[Tuple[str],
                             str,
                             None] = webview.windows[0].create_file_dialog(
                                 webview.SAVE_DIALOG, file_types=file_types, save_filename="diagram.scruml", directory=home_path
                             )
        file_path: str = ""

        # Different platforms do different things here, why????
        if not dialog_result:
            return ""
        elif isinstance(dialog_result, Tuple[str]):
            file_path = dialog_result[0]
        elif isinstance(dialog_result, str):
            file_path = dialog_result

        # Make sure the user selected a file
        if len(file_path) == 0:
            return ""

        # Save file and return status message
        if uml_filesystem_io.save_diagram(self.__diagram, file_path):
            return "Diagram successfully saved to: {}".format(file_path)
        else:
            return "Failed to save diagram to: {}".format(file_path)

    # ----------
    # Class functions

    # ----------
    # addClass

    def addClass(self, class_properties: Dict[str, str]) -> str:
        class_name: str = class_properties["class_name"]
        x: str = class_properties["x"]
        y: str = class_properties["y"]
        if not self.__parse_class_identifier(class_properties["class_name"]):
            return "Class name is invalid. (Cannot contain whitespace or quotes, and cannot be surrounded by brackets.)"
        if not self.__diagram.add_class(class_properties["class_name"]):
            return (
                "Class "
                + class_properties["class_name"]
                + " already exists in the diagram."
            )
        self.__diagram.set_class_attribute(class_name, "[x]", x)
        self.__diagram.set_class_attribute(class_name, "[y]", y)
        return ""

    # ----------
    # removeClass

    def removeClass(self, class_name: str) -> None:
        if not self.__diagram.remove_class(class_name):
            raise Exception("Selected class not found in diagram: " + class_name)

    # ----------
    # Class attribute functions

    # ----------
    # setClassAttribute

    def setClassAttribute(
        self, class_attribute_properties: Dict[str, str]
    ) -> str:

        class_name: str = class_attribute_properties["class_name"]
        attribute_name: str = class_attribute_properties["attribute_name"]
        attribute_value: str = class_attribute_properties["attribute_value"]

        if not class_attribute_properties["ignore_naming_rules"] and not self.__parse_class_identifier(attribute_name):
            return "Attribute name is invalid. (Cannot contain whitespace or quotes, and cannot be surrounded by brackets.)"

        if not self.__diagram.set_class_attribute(
            class_name, attribute_name, attribute_value
        ):
            return (
                "Class "
                + class_name
                + " does not exist in the diagram. Unable to add attribute: "
                + attribute_name
            )

        return ""

    # ----------
    # removeClassAttribute

    def removeClassAttribute(self, class_name: str, attribute_name: str) -> str:

        if not self.__diagram.remove_class_attribute(class_name, attribute_name):
            return (
                "Attribute "
                + attribute_name
                + " not found in Class: "
                + class_name
            )

        return ""

    # ----------
    # getClassAttributes

    def getClassAttributes(self, class_name: str) -> Dict[str, str]:
        attr_dict: Optional[Dict[str, str]] = self.__diagram.get_class_attributes(
            class_name
        )
        if not attr_dict:
            raise Exception("Selected class not found in diagram: " + class_name)
        return attr_dict

    # ----------
    # Relationship functions

    # ----------
    # addRelationship

    def addRelationship(self, relationship_properties: Dict[str, str]) -> str:

        class_name_a: str = relationship_properties["class_name_a"]
        class_name_b: str = relationship_properties["class_name_b"]
        relationship_name: str = relationship_properties["relationship_name"]

        if not class_name_a in self.__diagram.get_all_class_names():
            return "Class " + class_name_a + " not found in the diagram."
        if not class_name_b in self.__diagram.get_all_class_names():
            return "Class " + class_name_b + " not found in the diagram."

        if not self.__diagram.add_relationship(
            class_name_a, class_name_b, relationship_name if len(relationship_name) > 0 else None
        ):
            return (
                "Relationship already exists: ["
                + class_name_a
                + ","
                + class_name_b
                + (("," + relationship_name) if relationship_name else "")
                + "]"
            )

        return ""

    # ----------
    # removeRelationship

    def removeRelationship(self, relationship_id: str) -> str:

        relationship_id_tuple: Optional[Tuple[str, str, Optional[str]]] = self.__parse_relationship_identifier(relationship_id)

        if not relationship_id_tuple:
            raise Exception("Invalid relationship identifier provided: " + relationship_id)

        class_name_a: str = relationship_id_tuple[0]
        class_name_b: str = relationship_id_tuple[1]
        relationship_name: Optional[str] = relationship_id_tuple[2]

        if not class_name_a in self.__diagram.get_all_class_names():
            return "Class " + class_name_a + " not found in the diagram."
        if not class_name_b in self.__diagram.get_all_class_names():
            return "Class " + class_name_b + " not found in the diagram."

        if not self.__diagram.remove_relationship(
                class_name_a, class_name_b, relationship_name
        ):
            return (
                "Relationship not found in diagram: [ "
                + class_name_a
                + ","
                + class_name_b
                + (("," + relationship_name) if relationship_name else "")
                + "]"
            )

        return ""

    # ----------
    # Relationship attribute functions

    # TODO: Sprint 3


# ----------
# activate


def activate(enable_debug: bool = False) -> None:
    """Activates the GUI context.
If 'enable_debug' is set to 'True', enables the web console."""

    api = __API()
    html_file = pkg_resources.resource_filename("scruml", "assets/scruml.html")

    if enable_debug:
        print("Developer console enabled!")

    webview.create_window(
        "ScrUML", html_file, min_size=(640, 480), js_api=api, confirm_close=True
    )

    webview.start(debug=enable_debug, gui="cef")
