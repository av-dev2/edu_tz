# Copyright (c) 2020, Aakvatech and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase

from edu_tz.edu_tz.nmb.api import get_fee_info


class TestNMBCallback(IntegrationTestCase):
	"""get_fee_info resolves a bank reference back to the document that owns it."""

	def test_unknown_reference_resolves_to_nothing(self):
		info = get_fee_info("no-such-reference")
		self.assertEqual(info["name"], "")
		self.assertEqual(info["doctype"], "")

	def test_reference_resolves_to_student_applicant_fees(self):
		company = frappe.db.get_value("Company", {}, "name")
		if not company:
			self.skipTest("no Company on this site")

		reference = "TSTREF001"
		doc = frappe.get_doc(
			{
				"doctype": "Student Applicant Fees",
				"company": company,
				"student_name": "Test Applicant",
				"posting_date": frappe.utils.today(),
				"due_date": frappe.utils.today(),
				"grand_total": 100,
				"bank_reference": reference,
			}
		)
		doc.insert(ignore_permissions=True, ignore_mandatory=True)
		doc.db_set("bank_reference", reference)
		doc.db_set("docstatus", 1)

		info = get_fee_info(reference)
		self.assertEqual(info["doctype"], "Student Applicant Fees")
		self.assertEqual(info["name"], doc.name)
