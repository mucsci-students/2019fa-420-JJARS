# ScrUML
# uml_context_gui.py
# Team JJARS
from typing import Dict
from typing import Optional
from typing import Tuple

import pkg_resources
import webview
from webview import Window

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
    # getDiagram

    def getDiagram(self, params: str) -> Dict[str, Dict[str, Dict[str, str]]]:
        """Returns a dictionary containing all diagram information"""

        response: Dict[str, Dict[str, Dict[str, str]]] = {}

        # Populate response dictionary with classes
        response["classes"] = {}
        for class_name in self.__diagram.get_all_class_names():
            response["classes"][class_name] = self.__diagram.get_class_attributes(class_name)

        # Populate response dictionary with relationships
        response["relationships"] = {}
        for class_pair in self.__diagram.get_all_relationship_pairs():
            class_pair_string: str = "[" + class_pair[0] + "," + class_pair[1] + "]"
            print(class_pair_string)
            response["relationships"][class_pair_string] = {}
            relationships: Dict[
                str, Dict[str, str]
            ] = self.__diagram.get_relationships_between(class_pair[0], class_pair[1])
            for relationship_name in relationships:
                if not relationship_name:
                    relationship_name = ""
                response["relationships"][class_pair_string][relationship_name] = {}
                # TODO: another for-each, relationship attributes, god DARNIT

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
    # Diagram file functions

    # ----------
    # newDiagramFile

    def newDiagramFile(self, params: str) -> None:
        """Creates a new, blank diagram."""
        # TODO: Add a confirmation prompt
        self.__diagram = UMLDiagram()

    # ----------
    # loadDiagramFile

    def loadDiagramFile(self, params: str) -> None:
        """Opens a file selector dialog and loads the selected diagram file."""
        file_types: Tuple[str, str] = (
            "ScrUML Files (*.scruml;*.yaml)",
            "All Filles (*.*)",
        )
        file_path: str = webview.windows[0].create_file_dialog(
            webview.OPEN_DIALOG, file_types=file_types
        )[0]
        # TODO: Add a confirmation prompt
        self.__diagram = uml_filesystem_io.load_diagram(file_path)

    # ----------
    # saveDiagramFile

    def saveDiagramFile(self, params: str) -> None:
        """Opens a file save dialog and saves to the specified diagram file."""
        file_types: Tuple[str, str] = (
            "ScrUML Files (*.scruml;*.yaml)",
            "All Filles (*.*)",
        )
        file_path: str = webview.windows[0].create_file_dialog(
            webview.SAVE_DIALOG, file_types=file_types, save_filename="diagram.scruml"
        )[0]
        if uml_filesystem_io.save_diagram(self.__diagram, file_path):
            print("Diagram successfully saved to '{}'".format(file_path))
        else:
            print("Failed to save diagram to '{}'".format(file_path))

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
                'Class "'
                + class_properties["class_name"]
                + '" already exists in the diagram.'
            )
        self.__diagram.set_class_attribute(class_name, "[x]", x)
        self.__diagram.set_class_attribute(class_name, "[y]", y)
        return ""

    # ----------
    # removeClass

    def removeClass(self, class_name: str) -> None:
        if not self.__diagram.remove_class(
            class_name
        ):
            raise Exception("Selected class not found in diagram: " + class_name)

    # ----------
    # Class attribute functions

    # ----------
    # setClassAttribute

    def setClassAttribute(
        self, class_name: str, attribute_name: str, attribute_value: str
    ) -> None:
        if not self.__parse_class_identifier(attribute_name):
            return "Attribute name is invalid (cannot contain whitespace nor be surrounded by brackets."
        if not self.__diagram.set_class_attribute(
            class_name, attribute_name, attribute_value
        ):
            return (
                "Class '"
                + class_name
                + "' does not exist in the diagram. Unable to add Attribute '"
                + attribute_name
                + "'"
            )
        return ""

    # ----------
    # removeClassAttribute

    def removeClassAttribute(self, class_name: str, attribute_name: str) -> None:
        if not self.__diagram.remove_class_attribute(class_name, attribute_name):
            return (
                "Attribute '"
                + attribute_name
                + "' not found in Class '"
                + class_name
                + "'"
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

    def addRelationship(
        self, relationship_properties: Dict[str, str]
    ) -> str:

        class_name_a: str = relationship_properties["class_name_a"]
        class_name_b: str = relationship_properties["class_name_b"]
        relationship_name: Optional[str] = relationship_properties["relationship_name"]

        if not class_name_a in self.__diagram.get_all_class_names():
            return "Class " + class_name_a + " not found in the diagram."
        if not class_name_b in self.__diagram.get_all_class_names():
            return "Class " + class_name_b + " not found in the diagram."

        if len(relationship_name) == 0:
            relationship_name = None

        if not self.__diagram.add_relationship(
            class_name_a, class_name_b, relationship_name
        ):
            return (
                "Relationship already exists: ["
                + class_name_a
                + ","
                + class_name_b
                + (( "," + relationship_name ) if relationship_name else "")
                + "]"
            )

        return ""

    # ----------
    # removeRelationship

    def removeRelationship(
        self, class_name_a: str, class_name_b: str, relationship_name: str
    ) -> str:
        rel_name_arg: Optional[str] = None
        if len(relationship_name) != 0:
            rel_name_arg = relationship_name
        if not self.__diagram.remove_relationship(
            class_name_a, class_name_b, rel_name_arg
        ):
            return (
                "Relationship not found in diagram: [ "
                + class_name_a
                + ", "
                + class_name_b
                + ", "
                + relationship_name
                + "]"
            )
        return ""

    # ----------
    # Relationship attribute functions

    # TODO: Sprint 3


# ----------
# activate

def activate() -> None:
    """Activates the GUI context."""

    api = __API()
    html_file = pkg_resources.resource_filename("scruml", "assets/scruml.html")

    webview.create_window(
        "ScrUML",
        html_file,
        min_size=(640, 480),
        js_api=api,
        confirm_close=True)

    webview.start(debug=True,
                  gui="cef")
