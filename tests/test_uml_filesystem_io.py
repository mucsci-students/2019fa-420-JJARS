# SCRuml
# uml_file_test.py
# Team JJARS
import os

from scruml.uml_diagram import UMLDiagram
from scruml.uml_filesystem_io import uml_filesystem_io_load
from scruml.uml_filesystem_io import uml_filesystem_io_save


def test_save() -> None:
    umld: UMLDiagram = UMLDiagram()
    current_path: str = os.getcwd()

    assert umld.add_class("ClassSave") == "ClassSave"
    assert uml_filesystem_io_save(umld, current_path + "/tests.yaml") == True


def test_load() -> None:
    umld: UMLDiagram = UMLDiagram()
    current_path: str = os.getcwd()

    assert umld.add_class("ClassLoad") == "ClassLoad"
    assert uml_filesystem_io_save(umld, current_path + "/tests.yaml") == True
    assert uml_filesystem_io_load(umld, current_path + "tests.yaml") == True
    assert umld.add_class("ClassLoad") == None
