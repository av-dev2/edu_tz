import json
import os

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "custom_fields_json")
DISALLOWED_FIELDS = {
	"name",
	"owner",
	"creation",
	"modified",
	"modified_by",
	"docstatus",
	"idx",
	"is_system_generated",
	"__last_sync_on",
}


def execute():
	for file_name in sorted(os.listdir(FOLDER)):
		if file_name.endswith(".json"):
			create_fields_from_json(load_json(file_name))


def load_json(file_name):
	# nosemgrep: frappe-security-file-traversal -- reads only this app's bundled json
	with open(os.path.join(FOLDER, file_name)) as file:
		return json.load(file)


def create_fields_from_json(custom_fields):
	"""Creates the fields grouped by DocType, skipping DocTypes missing on the site."""
	field_keys = set(frappe.get_meta("Custom Field").get_valid_columns()) - DISALLOWED_FIELDS
	fields_by_doctype = {}
	for custom_field in custom_fields:
		doctype = custom_field["dt"]
		if not frappe.db.exists("DocType", doctype):
			continue
		field = {key: custom_field.get(key) for key in field_keys}
		fields_by_doctype.setdefault(doctype, []).append(field)

	if fields_by_doctype:
		create_custom_fields(fields_by_doctype, update=False)


@frappe.whitelist()
def export_custom_fields(docnames: str):
	custom_fields = []
	for docname in frappe.parse_json(docnames):
		doc = frappe.get_doc("Custom Field", docname)
		custom_fields.append(doc.as_dict(convert_dates_to_str=True, no_default_fields=True, no_nulls=True))
	return str(custom_fields)
