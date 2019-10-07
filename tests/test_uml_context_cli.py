# ScrUML
# test_uml_context_cli.py
# Team JJARS
# type: ignore
from pathlib import Path

from scruml.uml_context_cli import __UMLShell
from scruml.uml_diagram import UMLDiagram


def test_add_and_remove() -> None:
    shell: __UMLShell = __UMLShell()
    shell._UMLShell__diagram = UMLDiagram()

    shell.onecmd("add classA")
    shell.onecmd("add classB")
    shell.onecmd("add [invalidclass]")
    shell.onecmd("add invalid class")
    shell.onecmd("add [classA,classB]")
    shell.onecmd("add [classA,classB,myname]")
    shell.onecmd("add [[invalidrelationship],invalid class]")
    shell.onecmd("add [invalid class,[invalidrelationship],somename]")

    assert not shell._UMLShell__diagram.add_class("classA")
    assert not shell._UMLShell__diagram.add_class("classB")
    assert shell._UMLShell__diagram.get_all_class_names() == ["classA", "classB"]

    shell.onecmd("remove classA")
    shell.onecmd("remove classB")
    shell.onecmd("remove [invalidclass]")
    shell.onecmd("remove invalid class")
    shell.onecmd("remove [classA,classB]")
    shell.onecmd("remove [classA,classB,myname]")
    shell.onecmd("remove [[invalidrelationship],invalid class]")
    shell.onecmd("remove [invalid class,[invalidrelationship],somename]")

    assert shell._UMLShell__diagram.get_all_class_names() == []


def test_rename() -> None:
    shell: __UMLShell = __UMLShell()
    shell._UMLShell__diagram = UMLDiagram()

    shell.onecmd("add classA")
    shell.onecmd("add classB")
    shell.onecmd("rename classA classC")

    assert shell._UMLShell__diagram.get_all_class_names() == ["classC", "classB"]

    shell.onecmd("rename classB")
    assert shell._UMLShell__diagram.get_all_class_names() == ["classC", "classB"]

    shell.onecmd("remove classB")
    shell.onecmd("remove classC")
    shell.onecmd("add classA")
    shell.onecmd("rename classA [classB]")

    assert shell._UMLShell__diagram.get_all_class_names() == ["classA"]


def test_complete() -> None:
    shell: __UMLShell = __UMLShell()
    shell._UMLShell__diagram = UMLDiagram()

    shell.onecmd("add lcassC")
    shell.onecmd("add abc")
    shell.onecmd("add classA")
    shell.onecmd("add classB")
    shell.onecmd("add class12")

    assert shell.complete_remove("clas", "remove clas", 7, 11) == [
        "classA",
        "classB",
        "class12",
    ]
    assert shell.complete_remove("lcas", "remove clas", 7, 11) == ["lcassC"]
    assert shell.complete_remove("nart", "remove clas", 7, 11) == []

    assert shell.complete_rename("clas", "rename clas", 7, 11) == [
        "classA",
        "classB",
        "class12",
    ]
    assert shell.complete_rename("lcas", "rename clas", 7, 11) == ["lcassC"]
    assert shell.complete_rename("nart", "rename clas", 7, 11) == []


def test_save_and_load(tmp_path: Path):
    shell: __UMLShell = __UMLShell()
    shell._UMLShell__diagram = UMLDiagram()
    file_path: str = str(tmp_path / "saveandloadtest.yaml")

    shell.onecmd("add classToLoad")
    assert shell._UMLShell__diagram.get_all_class_names() == ["classToLoad"]

    shell.onecmd("save " + file_path)

    shell.onecmd("remove classToLoad")
    assert shell._UMLShell__diagram.get_all_class_names() == []

    shell.onecmd("load " + file_path)
    assert shell._UMLShell__diagram.get_all_class_names() == ["classToLoad"]


def test_misc() -> None:
    shell: __UMLShell = __UMLShell()
    shell._UMLShell__diagram = UMLDiagram()

    shell.onecmd("print")
    shell.onecmd("help")
    shell.onecmd("help identifiers")
