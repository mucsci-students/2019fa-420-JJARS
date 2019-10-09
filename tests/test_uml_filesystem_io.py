# SCRuml
# uml_file_test.py
# Team JJARS
import os
from pathlib import Path

from scruml import uml_filesystem_io
from scruml.uml_diagram import UMLDiagram


def test_save(tmp_path: Path) -> None:
    diagram: UMLDiagram = UMLDiagram()
    file_path: str = str(tmp_path / "savetest.yaml")
    assert diagram.add_class("SavedClassName") == "SavedClassName"
    assert uml_filesystem_io.save_diagram(diagram, file_path)
    invalid_file_path: str = str(
        tmp_path
        / '\\乃工厶 匚卄凵𠘨厶凵丂!//#$!(*"🕳️🚶"*)Ỏ̷͖͈̞̩͎̻̫̫̜͉̠̫͕̭̭̫̫̹̗̹͈̼̠̖͍͚̥͈̮̼͕̠̤̯̻̥̬̗̼̳̤̳̬̪̹͚̞̼̠͕̼̠̦͚̫͔̯̹͉͉̘͎͕̼̣̝͙̱̟̹̩̟̳̦̭͉̮̖̭̣̣̞̙̗̜̺̭̻̥͚͙̝̦̲̱͉͖͉̰̦͎̫̣̼͎͍̠̮͓̹̹͉̤̰̗̙͕͇͔̱͕̭͈̳̗̭͔̘̖̺̮̜̠͖̘͓̳͕̟̠̱̫̤͓͔̘̰̲͙͍͇̙͎̣̼̗̖͙̯͉̠̟͈͍͕̪͓̝̩̦̖̹̼̠̘̮͚̟͉̺̜͍͓̯̳'
    )
    assert not uml_filesystem_io.save_diagram(diagram, invalid_file_path)


def test_save_and_load(tmp_path: Path) -> None:
    diagram: UMLDiagram = UMLDiagram()
    file_path: str = str(tmp_path / "saveandloadtest.yaml")
    assert diagram.add_class("ClassToLoad") == "ClassToLoad"
    assert uml_filesystem_io.save_diagram(diagram, file_path)
    diagram = uml_filesystem_io.load_diagram(file_path)
    assert "ClassToLoad" in diagram.get_all_class_names()
