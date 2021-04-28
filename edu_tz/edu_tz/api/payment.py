from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import getdate
from csf_tz import console


def on_submit(doc, method):
    create_sales_invoice(doc)


def create_sales_invoice(doc):
    if (
        doc.party_type == "Student"
        and len(doc.references) > 0
        and doc.references[0].reference_doctype == "Fees"
    ):
        fees_doc = frappe.get_doc("Fees", doc.references[0].reference_name)
        item_name = fees_doc.components[0].description
        income_account = fees_doc.sales_invoice_income_account
        customer = frappe.get_value("Student", doc.party, "customer")
        if not customer:
            frappe.throw(_("Please set Customer in Student record"))

        sales_invoice = frappe.new_doc("Sales Invoice")
        sales_invoice.customer = customer
        sales_invoice.remarks = "Payment Entry: " + doc.name
        sales_invoice.due_date = getdate()
        sales_invoice.company = doc.company
        sales_invoice.fees = fees_doc.name
        sales_invoice.payment_entry = doc.name

        sales_invoice.append(
            "items",
            {
                # "item_code": item_code,
                "item_name": item_name,
                "description": item_name,
                "qty": 1,
                "uom": "Unit",
                "conversion_factor": 1,
                "rate": doc.paid_amount,
                "amount": doc.paid_amount,
            },
        )

        sales_invoice.flags.ignore_permissions = True
        frappe.flags.ignore_account_permission = True
        sales_invoice.set_missing_values()
        console(sales_invoice)
        sales_invoice.save(ignore_permissions=True)
        frappe.msgprint(
            _("Draft Sales Invoice created {0}").format(sales_invoice.name), alert=True
        )
        return sales_invoice.name
