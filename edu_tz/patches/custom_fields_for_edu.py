import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
    fields = {
        "Student": [
            {
                "fieldname": "bank",
                "fieldtype": "Select",
                "insert_after": "student_applicant",
                "label": "Bank",
                "options": "\n NMB Bank",
                "translatable": 1,
            },
        ],
        "Student Applicant": [
            {
                "allow_on_submit": 1,
                "fieldname": "student_applicant_fee",
                "fieldtype": "Data",
                "insert_after": "paid",
                "label": "Student Applicant Fee",
                "read_only": 1,
                "translatable": 1,
            },
            {
                "allow_on_submit": 1,
                "fieldname": "bank_reference",
                "fieldtype": "Data",
                "insert_after": "student_applicant_fee",
                "label": "Bank Reference",
                "read_only": 1,
                "translatable": 1,
            },
            {
                "fieldname": "fee_structure",
                "fieldtype": "Link",
                "insert_after": "application_date",
                "label": "Fee Structure",
                "options": "Fee Structure",
                "reqd": 1,
            },
            {
                "fieldname": "program_enrollment",
                "fieldtype": "Link",
                "insert_after": "fee_structure",
                "label": "Program Enrollment",
                "options": "Program Enrollment",
            },
        ],
        "Program Fee": [
            {
                "fetch_from": "fee_structure.default_fee_category",
                "fieldname": "default_fee_category",
                "fieldtype": "Link",
                "in_list_view": 1,
                "insert_after": "due_date",
                "label": "Default Fee Category",
                "options": "Fee Category",
            },
        ],
        "Program": [
            {
                "fieldname": "fees",
                "fieldtype": "Section Break",
                "insert_after": "courses",
                "label": "Fees",
            },
            {
                "label": "Company",
                "fieldname": "company",
                "insert_after": "program_abbreviation",
                "fieldtype": "Link",
            },
            {
                "label": "Program Fee",
                "fieldname": "program_fee",
                "insert_after": "fees",
                "fieldtype": "Table",
                "options": "Program Fee",
            },
        ],
        "Fees": [
            {
                "allow_on_submit": 1,
                "fieldname": "callback_token",
                "fieldtype": "Data",
                "insert_after": "healthcare_practitioner",
                "label": "Callback Token",
                "read_only": 1,
                "translatable": 1,
            },
            {
                "allow_on_submit": 1,
                "fieldname": "bank_reference",
                "fieldtype": "Data",
                "insert_after": "send_payment_request",
                "label": "Bank Reference",
                "read_only": 1,
                "translatable": 1,
            },
            {
                "fetch_from": "company.abbr",
                "fieldname": "abbr",
                "fieldtype": "Data",
                "insert_after": "company",
                "label": "Abbr",
                "read_only": 1,
                "translatable": 1,
            },
            {
                "fieldname": "from_date",
                "fieldtype": "Date",
                "insert_after": "vehicle",
                "label": "From Date",
            },
            {
                "fieldname": "to_date",
                "fieldtype": "Date",
                "insert_after": "from_date",
                "label": "To Date",
            },
        ],
        "Fee Structure": [
            {
                "allow_on_submit": 1,
                "fieldname": "default_fee_category",
                "fieldtype": "Link",
                "insert_after": "student_category",
                "label": "Default Fee Category",
                "options": "Fee Category",
            },
        ],
    }
    create_custom_fields(fields, update=True)
