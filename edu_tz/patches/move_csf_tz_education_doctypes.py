"""Reassigns the DocTypes that moved out of csf_tz to the Edu Tz module."""

import frappe

MOVED_DOCTYPES = ("Student Applicant Fees", "NMB Callback")


def execute():
	for doctype in MOVED_DOCTYPES:
		if frappe.db.exists("DocType", doctype):
			frappe.db.set_value("DocType", doctype, "module", "Edu Tz", update_modified=False)
