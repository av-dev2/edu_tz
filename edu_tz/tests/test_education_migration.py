"""Guards the move of the education and NMB code out of csf_tz into edu_tz."""

import frappe
from frappe.tests import IntegrationTestCase

from edu_tz.patches.custom_fields import create_custom_fields

MOVED_DOCTYPES = ("Student Applicant Fees", "NMB Callback")

COMPANY_NMB_FIELDS = (
    "education_section",
    "send_fee_details_to_bank",
    "fee_bank_account",
    "student_applicant_fees_revenue_account",
    "nmb_series",
    "nmb_username",
    "nmb_password",
    "nmb_url",
)


class TestEducationMigration(IntegrationTestCase):
    def test_moved_doctypes_belong_to_edu_tz(self):
        for doctype in MOVED_DOCTYPES:
            self.assertEqual(frappe.db.get_value("DocType", doctype, "module"), "Edu Tz")

    def test_company_nmb_custom_fields_exist(self):
        for fieldname in COMPANY_NMB_FIELDS:
            self.assertTrue(
                frappe.db.exists("Custom Field", f"Company-{fieldname}"),
                f"Company-{fieldname} was not created",
            )

    def test_education_custom_fields_exist(self):
        for name in ("Fees-callback_token", "Fees-bank_reference", "Fees-abbr"):
            self.assertTrue(frappe.db.exists("Custom Field", name), f"{name} was not created")

    def test_loader_is_idempotent(self):
        before = frappe.db.count("Custom Field")
        create_custom_fields.execute()
        self.assertEqual(frappe.db.count("Custom Field"), before)

    def test_loader_skips_doctypes_that_are_not_installed(self):
        """The loader must not raise on a bench without the education app."""
        fields = [{"dt": "No Such DocType", "fieldname": "x", "fieldtype": "Data", "label": "X"}]
        create_custom_fields.create_fields_from_json(fields)
        self.assertFalse(frappe.db.exists("Custom Field", "No Such DocType-x"))

    def test_csf_tz_callback_shim_forwards(self):
        from csf_tz import bank_api

        from edu_tz.edu_tz.nmb import api

        self.assertIn("edu_tz", frappe.get_installed_apps())
        self.assertTrue(callable(bank_api.receive_callback))
        self.assertTrue(callable(api.receive_callback))

    def test_get_fee_schedule_filters_by_academic_year(self):
        from edu_tz.edu_tz.overrides.program_enrollment import get_fee_schedule

        self.assertEqual(get_fee_schedule("No Such Program", "2099-2100"), [])
