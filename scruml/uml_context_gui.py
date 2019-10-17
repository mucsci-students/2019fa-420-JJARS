# ScruML
# uml_context_gui.py
# Team JJARS
import pkg_resources
import webview


def activate() -> None:
    html_file = pkg_resources.resource_filename("scruml", "assets/scruml.html")
    webview.create_window("ScrUML", html_file, min_size=(640, 480))
    webview.start(debug=True)
