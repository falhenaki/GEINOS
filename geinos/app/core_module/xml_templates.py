from xml.etree import ElementTree as et


def generate_jinja(xml_file, replacements):
	"""
	method to replace the value of all attributes with a tag in replacements with jinja2 tags
	:param xml_file: file to perform replacements on
	:param replacements: xml tags that should have their values replaced with jinja2 tags
	:return: xml file with desired replacements converted to jinja2 tags
	"""
	tree = et.parse(xml_file)
	root = tree.getroot()
	for replacement in replacements:
		for occurrence in root.findall(replacement):
			occurrence.text = '{{' + replacement + '}}'
	tree.write(xml_file)
	return xml_file