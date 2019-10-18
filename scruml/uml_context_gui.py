# ScruML
# uml_context_gui.py
# Team JJARS
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

    def loadDiagramFile(self, params: str) -> None:
        """Opens a file selector dialog and loads the selected diagram file."""
        file_types: Tuple[str, str] = (
            "ScrUML Files (*.scruml;*.yaml)",
            "All Filles (*.*)",
        )
        print(
            webview.windows[0].create_file_dialog(
                webview.OPEN_DIALOG, file_types=file_types
            )
        )

    def saveDiagramFile(self, params: str) -> None:
        """Opens a file save dialog and saves to the specified diagram file."""
        file_types: Tuple[str, str] = (
            "ScrUML Files (*.scruml;*.yaml)",
            "All Filles (*.*)",
        )
        print(
            webview.windows[0].create_file_dialog(
                webview.SAVE_DIALOG,
                file_types=file_types,
                save_filename="diagram.scruml",
            )
        )


def activate() -> None:
    """Activates the GUI context."""
    api = __API()
    html_file = pkg_resources.resource_filename("scruml", "assets/scruml.html")
    webview.create_window(
        "ScrUML", html_file, min_size=(640, 480), js_api=api, confirm_close=True
    )
    webview.start(debug=True)
