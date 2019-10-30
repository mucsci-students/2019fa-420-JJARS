# ScrUML
# test_uml_context_gui.py
# Team JJARS
import pytest

import scruml.uml_context_gui
from scruml.uml_context_gui import __API
from scruml.uml_diagram import UMLDiagram


def test_activate() -> None:
    # TODO: To be updated with the context_gui module
    # scruml.uml_context_gui.activate()
    pass


def test_add_and_remove_class() -> None:
    api: __API = __API()
    api.__diagram = UMLDiagram()

    assert api.__diagram.add_class("classA")
    assert api.__diagram.add_class("classB")
    assert sorted(api.__diagram.get_all_class_names()) == ["classA", "classB"]


# assert api.__diagram.get_all_class_names() == []
