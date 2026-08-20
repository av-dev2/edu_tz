# Copyright (c) 2020, Aakvatech and Contributors
# See license.txt

from unittest.mock import patch

import frappe
from frappe.tests import IntegrationTestCase


class TestStudentApplicantFees(IntegrationTestCase):
	"""after_insert stamps the bank fields only when the company opts into the NMB flow."""

	def setUp(self):
		self.company = frappe.db.get_value("Company", {}, "name")
		if not self.company:
			self.skipTest("no Company on this site")

	def _make(self):
		return frappe.get_doc(
			{
				"doctype": "Student Applicant Fees",
				"company": self.company,
				"student_name": "Test Applicant",
				"posting_date": frappe.utils.today(),
				"due_date": frappe.utils.today(),
				"grand_total": 100,
			}
		)

	def test_bank_fields_set_when_enabled(self):
		frappe.db.set_value("Company", self.company, "send_fee_details_to_bank", 1)
		frappe.db.set_value("Company", self.company, "nmb_series", "TST")

		doc = self._make()
		doc.insert(ignore_permissions=True, ignore_mandatory=True)

		self.assertTrue(doc.callback_token)
		self.assertTrue(doc.bank_reference)
		self.assertTrue(doc.bank_reference.startswith("TST"))

	def test_bank_fields_skipped_when_disabled(self):
		frappe.db.set_value("Company", self.company, "send_fee_details_to_bank", 0)

		doc = self._make()
		doc.insert(ignore_permissions=True, ignore_mandatory=True)

		self.assertFalse(doc.callback_token)
		self.assertFalse(doc.bank_reference)

	def test_missing_series_throws(self):
		frappe.db.set_value("Company", self.company, "send_fee_details_to_bank", 1)
		frappe.db.set_value("Company", self.company, "nmb_series", "")

		with self.assertRaises(frappe.ValidationError):
			self._make().insert(ignore_permissions=True, ignore_mandatory=True)

	def test_submit_sends_to_bank_only_when_enabled(self):
		frappe.db.set_value("Company", self.company, "send_fee_details_to_bank", 0)
		doc = self._make()
		doc.insert(ignore_permissions=True, ignore_mandatory=True)

		with patch(
			"edu_tz.edu_tz.doctype.student_applicant_fees.student_applicant_fees.invoice_submission"
		) as sent:
			doc.submit()
		sent.assert_not_called()
