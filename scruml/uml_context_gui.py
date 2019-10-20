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


class __API:
    """Provides an API to the JavaScript running in the GUI window.
Can be called from the JavaScript as such: pywebview.api.FUNCTIONNAME( ... )"""

    __diagram: UMLDiagram = UMLDiagram()

    def getDiagram(self, params: str) -> Dict[str, str]:
        """Returns a dictionary containing all diagram information"""

        pass

    def __parse_class_identifier(self, ident: str) -> Optional[str]:
        """Returns valid class identifier on success, or None on failure
Valid class identifiers contain no whitespace and are not surrounded by brackets"""
        ident = ident.strip()
        if " " in ident:
            return None
        if ident.startswith("[") and ident.endswith("]"):
            return None
        return ident

    def newDiagramFile(self, params: str) -> None:
        """Creates a new, blank diagram."""
        # TODO: Add a confirmation prompt
        self.__diagram = UMLDiagram()

    def loadDiagramFile(self, params: str) -> None:
        """Opens a file selector dialog and loads the selected diagram file."""
        file_types: Tuple[str, str] = (
            "ScrUML Files (*.scruml;*.yaml)",
            "All Filles (*.*)",
        )
        file_path: str = webview.windows[0].create_file_dialog(
            webview.OPEN_DIALOG, file_types=file_types
        )
        # TODO: Add a confirmation prompt
        self.__diagram = uml_filesystem_io.load_diagram(file_path)

    def saveDiagramFile(self, params: str) -> None:
        """Opens a file save dialog and saves to the specified diagram file."""
        file_types: Tuple[str, str] = (
            "ScrUML Files (*.scruml;*.yaml)",
            "All Filles (*.*)",
        )
        file_path: str = webview.windows[0].create_file_dialog(
            webview.SAVE_DIALOG, file_types=file_types, save_filename="diagram.scruml"
        )
        if uml_filesystem_io.save_diagram(self.__diagram, file_path):
            print("Diagram successfully saved to '{}'".format(file_path))
        else:
            print("Failed to save diagram to '{}'".format(file_path))

    def addClass(self, class_name: str) -> str:
        if not self.__parse_class_identifier(class_name):
            return "Class name is invalid (cannot contain whitespace nor be surrounded by brackets."
        if not self.__diagram.add_class(class_name):
            return 'Class "' + class_name + '" already exists in the diagram.'
        return ""

    def setClassCoordinates(self, class_name: str, x_pos: int, y_pos: int) -> None:
        self.__diagram.set_class_attribute(class_name, "[X Position]", str(x_pos))
        self.__diagram.set_class_attribute(class_name, "[Y Position]", str(y_pos))

    def getClassAttributes(self, class_name: str) -> Dict[str, str]:
        attr_dict: Optional[Dict[str, str]] = self.__diagram.get_class_attributes(
            class_name
        )
        if not attr_dict:
            raise Exception("Selected class not found in diagram: " + class_name)
        return attr_dict

    def completelyRemoveClass(self, class_name: str) -> None:
        if not self.__diagram.complete_remove(
            class_name
        ):  # TODO: make sure complete remove is implemented
            raise Exception("Selected class not found in diagram: " + class_name)

    def addRelationship(
        self, class_name_a: str, class_name_b: str, relationship_name: str
    ) -> str:
        rel_name_arg: Optional[str] = None
        if len(relationship_name) != 0:
            rel_name_arg = relationship_name
        if not self.__diagram.add_relationship(
            class_name_a, class_name_b, rel_name_arg
        ):
            return (
                "Class name(s) not found or relationship already exists: [ "
                + class_name_a
                + ", "
                + class_name_b
                + ", "
                + relationship_name
                + "]"
            )
        return ""

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


def activate() -> None:
    """Activates the GUI context."""
    api = __API()
    html_file = pkg_resources.resource_filename("scruml", "assets/scruml.html")
    webview.create_window(
        "ScrUML", html_file, min_size=(640, 480), js_api=api, confirm_close=True
    )
    webview.start(debug=True)
