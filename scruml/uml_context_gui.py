# ScrUML
# uml_context_gui.py
# Team JJARS
from os import path
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pkg_resources
import webview

from scruml import uml_filesystem_io
from scruml import uml_utilities
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

            class_attributes: Optional[
                Dict[str, str]
            ] = self.__diagram.get_class_attributes(class_name)

            if class_attributes is not None:
                response[class_name] = class_attributes
            else:
                raise Exception("Class not found in diagram: " + class_name)

        return response

    # ----------
    # getAllRelationships

    def getAllRelationships(self, params: str) -> Dict[str, Dict[str, str]]:
        """Returns a dictionary containing all relationship infromation in the diagram.
Structure: dictionary[classPair][attributeName] == attributeValue"""

        response: Dict[str, Dict[str, str]] = {}

        # Populate response dictionary with relationships
        for class_pair in self.__diagram.get_all_relationship_pairs():

            relationship_attributes: Optional[
                Dict[str, str]
            ] = self.__diagram.get_relationship_between(class_pair[0], class_pair[1])

            if relationship_attributes is not None:
                relationship_id: str = uml_utilities.stringify_relationship_identifier(
                    class_pair[0], class_pair[1]
                )
                response[relationship_id] = relationship_attributes
            else:
                raise Exception(
                    "Relationship not found in diagram: {}".format(
                        uml_utilities.stringify_relationship_identifier(
                            class_pair[0], class_pair[1]
                        )
                    )
                )

        return response

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
        dialog_result: Union[Tuple[str], str, None] = webview.windows[
            0
        ].create_file_dialog(webview.OPEN_DIALOG, file_types=file_types)
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
        dialog_result: Union[Tuple[str], str, None] = webview.windows[
            0
        ].create_file_dialog(
            webview.SAVE_DIALOG,
            file_types=file_types,
            save_filename="diagram.scruml",
            directory=home_path,
        )
        file_path: str = ""

        # Different platforms do different things here, why????
        if not dialog_result:
            return ""
        elif isinstance(dialog_result, tuple):
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
        if not uml_utilities.parse_class_identifier(class_properties["class_name"]):
            return "Class name is invalid. (Cannot contain whitespace or quotes, and cannot be surrounded by brackets.)"
        if not self.__diagram.add_class(class_name):
            return "Class " + class_name + " already exists in the diagram."
        self.__diagram.set_class_attribute(class_name, "[x]", x)
        self.__diagram.set_class_attribute(class_name, "[y]", y)
        return ""

    # ----------
    # removeClass

    def removeClass(self, class_name: str) -> None:
        if not self.__diagram.remove_class(class_name):
            raise Exception("Selected class not found in diagram: " + class_name)

    # ----------
    # renameClass

    def renameClass(self, class_properties: Dict[str, str]) -> str:
        old_class_name: str = class_properties["old_class_name"]
        new_class_name: str = class_properties["new_class_name"]
        if not uml_utilities.parse_class_identifier(old_class_name):
            return "Old class name is invalid. (Cannot contain whitespace or quotes, and cannot be surrounded by brackets.)"
        if not uml_utilities.parse_class_identifier(new_class_name):
            return "New class name is invalid. (Cannot contain whitespace or quotes, and cannot be surrounded by brackets.)"
        if not self.__diagram.rename_class(old_class_name, new_class_name):
            return "Class " + new_class_name + " already exists in the diagram."
        return ""

    # ----------
    # Class attribute functions

    # ----------
    # setClassAttribute

    def setClassAttribute(self, class_attribute_properties: Dict[str, str]) -> str:

        class_name: str = class_attribute_properties["class_name"]
        attribute_name: str = class_attribute_properties["attribute_name"]
        attribute_value: str = class_attribute_properties["attribute_value"]

        if (
            not "ignore_naming_rules" in class_attribute_properties
            and not uml_utilities.parse_class_identifier(attribute_name)
        ):
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
            return "Attribute " + attribute_name + " not found in Class: " + class_name

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

        if not class_name_a in self.__diagram.get_all_class_names():
            return "Class " + class_name_a + " not found in the diagram."
        if not class_name_b in self.__diagram.get_all_class_names():
            return "Class " + class_name_b + " not found in the diagram."

        if not self.__diagram.add_relationship(class_name_a, class_name_b):
            return "Relationship already exists: {}".format(
                uml_utilities.stringify_relationship_identifier(
                    class_name_a, class_name_b
                )
            )

        return ""

    # ----------
    # removeRelationship

    def removeRelationship(self, relationship_id: str) -> str:

        relationship_id_tuple: Optional[
            Tuple[str, str]
        ] = uml_utilities.parse_relationship_identifier(relationship_id)

        if not relationship_id_tuple:
            raise Exception(
                "Invalid relationship identifier provided: " + relationship_id
            )

        class_name_a: str = relationship_id_tuple[0]
        class_name_b: str = relationship_id_tuple[1]

        if not class_name_a in self.__diagram.get_all_class_names():
            return "Class " + class_name_a + " not found in the diagram."
        if not class_name_b in self.__diagram.get_all_class_names():
            return "Class " + class_name_b + " not found in the diagram."

        if not self.__diagram.remove_relationship(class_name_a, class_name_b):
            return "Relationship not found in diagram: {}".format(
                uml_utilities.stringify_relationship_identifier(
                    class_name_a, class_name_b
                )
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
        "ScrUML", html_file, min_size=(1024, 720), js_api=api, confirm_close=True
    )

    webview.start(debug=enable_debug, gui="cef")
