// edu_tz override for Payment Reconciliation
// Fixes root_type filter on receivable_payable_account to correctly treat
// ALL "Receivable" party types (e.g. Customer, Student) as "Asset",
// not just "Customer" as ERPNext core hard-codes.
// See: erpnext/accounts/doctype/payment_reconciliation/payment_reconciliation.js L30

frappe.ui.form.on("Payment Reconciliation", {
	onload: function (frm) {
		frm.set_query("receivable_payable_account", () => {
			return {
				filters: {
					company: frm.doc.company,
					is_group: 0,
					account_type: frappe.boot.party_account_types[frm.doc.party_type],
					root_type:
						frappe.boot.party_account_types[frm.doc.party_type] == "Receivable"
							? "Asset"
							: "Liability",
				},
			};
		});
	},
});
