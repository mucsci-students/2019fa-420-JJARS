#SCRuml
#uml_filesystem_io.py
#Team JJARS

import yaml
from scruml.uml_diagram import UMLDiagram

def uml_filesystem_io_save(UMLDiagram, str):
# -> bool
		with open(str,'wb') as f:
		if True:
			yaml.dump(UMLDiagram, f, protocol=-1)
			return true
		else:
			return false

def uml_filesystem_io_load(UMLDiagram, str ):
# -> bool
		is_open = open(str, 'rb')
		UMLDiagram = yaml.load
		if UMLDiagram is {}:
			return false
		else:
			return true
