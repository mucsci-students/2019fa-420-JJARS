# SCRuml
# uml_filesystem_io.py
# Team JJARS
import yaml

from scruml.uml_diagram import UMLDiagram


def save_diagram(diagram: UMLDiagram, file_path: str) -> bool:
    with open(file_path, "w") as f:
        if f:
            yaml.dump(diagram, f)
            return True
        return False


def load_diagram(file_path: str) -> UMLDiagram:
    with open(file_path, "r") as f:
        diagram: UMLDiagram = yaml.load(f)
        return diagram
