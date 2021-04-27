from __future__ import unicode_literals
import frappe
from frappe import _
from erpnext import get_default_currency


def after_insert(doc, method):
    create_customer(doc)


def validate(doc, method):
    if not doc.customer and not doc.is_new():
        doc.customer = create_customer(doc)


def create_customer(doc):
    customer = frappe.get_doc(
        {
            "doctype": "Customer",
            "customer_name": doc.title,
            "customer_group": "Student"
            or frappe.db.get_single_value("Selling Settings", "customer_group"),
            "territory": frappe.db.get_single_value("Selling Settings", "territory"),
            "customer_type": "Individual",
            "default_currency": get_default_currency(),
            "default_price_list": frappe.db.get_single_value(
                "Selling Settings", "selling_price_list"
            ),
            "language": frappe.db.get_single_value("System Settings", "language"),
            "student": doc.name,
        }
    ).insert(ignore_permissions=True, ignore_mandatory=True)

    frappe.db.set_value("Student", doc.name, "customer", customer.name)
    frappe.msgprint(_("Customer {0} is created.").format(customer.name), alert=True)
    return customer.name
