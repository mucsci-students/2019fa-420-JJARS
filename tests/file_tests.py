# SCRuml
# uml_file_test.py
# Team JJARS
from scruml.uml_diagram import UMLDiagram
from scruml.uml_filesystem_io import uml_filesystem_io_load
from scruml.uml_filesystem_io import uml_filesystem_io_save


def test_save() -> None:
    umld: UMLDiagram = UMLDiagram()

    assert umld.add_class("ClassSave") == "ClassSave"
    assert (
        uml_filesystem_io_save(
            umld,
            "C:/Users/Ryan Andrews/Documents/Software Engineering/JJARS/tests/tests.yaml",
        )
        == True
    )


def test_load() -> None:
    umld: UMLDiagram = UMLDiagram()

    assert umld.add_class("ClassLoad") == "ClassLoad"
    assert (
        uml_filesystem_io_save(
            umld,
            "C:/Users/Ryan Andrews/Documents/Software Engineering/JJARS/tests/tests.yaml",
        )
        == True
    )
    assert (
        uml_filesystem_io_load(
            umld,
            "C:/Users/Ryan Andrews/Documents/Software Engineering/JJARS/tests/tests.yaml",
        )
        == True
    )
    assert umld.add_class("ClassLoad") == None
