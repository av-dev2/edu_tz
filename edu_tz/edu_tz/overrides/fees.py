from typing import Any

import frappe
from erpnext.accounts.utils import unlink_ref_doc_from_payment_entries

from edu_tz.edu_tz.nmb.api import cancel_invoice


def set_fee_abbr(doc: Any, method: Any = None):
	doc.company = frappe.get_value("Fee Structure", doc.fee_structure, "company")
	if not frappe.get_value("Company", doc.company, "send_fee_details_to_bank"):
		return
	doc.abbr = frappe.get_value("Company", doc.company, "abbr")


def on_cancel_fees(doc: Any, method: Any = None):
	unlink_ref_doc_from_payment_entries(doc)
	cancel_invoice(doc, "before_cancel")
