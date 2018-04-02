from app.core_module import db_connector


def generate_jinja(xml_filename, replacements):
	"""
	method to replace the value of all attributes with a tag in replacements with jinja2 tags
	:param xml_file: file to perform replacements on
	:param replacements: xml tags that should have their values replaced with jinja2 tags
	:return: xml file with desired replacements converted to jinja2 tags
	"""
	xml_file = db_connector.get_file(xml_filename)
	with open(xml_file, 'r') as f:
		s = f.read()
	with open(xml_file, 'w') as fout:
		for replacement in replacements:
			s = s.replace(replacement, '{{' + replacement + '}}')
		fout.write(s)
		db_connector.replace_template(xml_filename, fout)
	return fout

def store_file(xml_filename, file):
	db_connector.add_file(xml_filename, file)

def get_file(xml_filename):
	return db_connector.get_file(xml_filename)