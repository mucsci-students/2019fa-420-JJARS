# SCRuml
# uml_file_test.py
# Team JJARS
import os

from scruml import uml_filesystem_io
from scruml.uml_diagram import UMLDiagram


def test_save() -> None:
    umld: UMLDiagram = UMLDiagram()
    current_path: str = os.getcwd()
    assert umld.add_class("ClassSave") == "ClassSave"
    assert (
        uml_filesystem_io.save_diagram(umld, current_path + "/tmp/tests.yaml") == True
    )


def test_load() -> None:
    umld: UMLDiagram = UMLDiagram()
    current_path: str = os.getcwd()
    assert umld.add_class("ClassLoad") == "ClassLoad"
    assert (
        uml_filesystem_io.save_diagram(umld, current_path + "/tmp/tests.yaml") == True
    )
    umld = uml_filesystem_io.load_diagram(current_path + "/tmp/tests.yaml")
    assert umld.add_class("ClassLoad") == None
