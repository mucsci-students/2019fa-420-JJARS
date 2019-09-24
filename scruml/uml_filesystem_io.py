#SCRuml
#uml_filesystem_io.py
#Team JJARS

import yaml
from uml_diagram import UMLDiagram

def uml_filesystem_io_save( diagram: UMLDiagram, file_path: str) -> bool:
		with open(file_path,'wb') as f:
			if f:
				yaml.dump(diagram, f, protocol=-1)
				return True
			return False

def uml_filesystem_io_load( diagram: UMLDiagram, file_path: str) -> bool:
		is_open = open(file_path, 'rb')
		diagram = yaml.load(is_open)
		if diagram is {}:
			return False
		return True


	


