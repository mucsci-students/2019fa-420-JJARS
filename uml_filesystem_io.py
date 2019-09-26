#SCRuml
#uml_filesystem_io.py
#Team JJARS

import yaml
#TODO: Fix problem with import statement
from scruml.uml_diagram import UMLDiagram

def uml_filesystem_io_save( diagram: UMLDiagram,file_path: str) -> bool:
		with open(file_path,'wb') as f:
			if True:
				yaml.dump(diagram, f, protocol=-1)
				return True
			else:
				return False

def uml_filesystem_io_load( diagram: UMLDiagram,file_path: str ) -> bool:
		is_open = open(file_path, 'rb')
		diagram = yaml.load( is_open)
		if UMLDiagram is {}:
			return False
		else:
			return True
