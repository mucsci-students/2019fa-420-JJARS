# SCRuml
# uml_filesystem_io.py
# Team JJARS
import yaml

from uml_diagram import UMLDiagram


def save_diagram(diagram: UMLDiagram, file_path: str) -> bool:
    try:
        with open(file_path, "w") as diagram_file:
            yaml.dump(diagram, diagram_file)
            return True
    except:
        return False


def load_diagram(file_path: str) -> UMLDiagram:
    with open(file_path, "r") as diagram_file:
        diagram: UMLDiagram = UMLDiagram()
        if diagram_file:
            diagram = yaml.full_load(diagram_file)
        return diagram
