import json
import os

import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "property_setters_json")


def execute():
	for file_name in sorted(os.listdir(FOLDER)):
		if file_name.endswith(".json"):
			create_property_setters_from_json(load_json(file_name))


def load_json(file_name):
	# nosemgrep: frappe-security-file-traversal -- reads only this app's bundled json
	with open(os.path.join(FOLDER, file_name)) as file:
		return json.load(file)


def create_property_setters_from_json(property_setters):
	"""Creates the missing setters, skipping DocTypes missing on the site."""
	existing = set(frappe.get_all("Property Setter", pluck="name", limit=0))
	for property_setter in property_setters:
		if property_setter["name"] in existing:
			continue
		if not frappe.db.exists("DocType", property_setter["doc_type"]):
			continue
		make_property_setter(
			doctype=property_setter["doc_type"],
			fieldname=property_setter.get("field_name"),
			property=property_setter["property"],
			value=property_setter["value"],
			property_type=property_setter["property_type"],
			for_doctype=property_setter["doctype_or_field"] == "DocType",
		)
