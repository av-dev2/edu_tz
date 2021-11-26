// Copyright (c) 2016, Aakvatech and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Fee Collection Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"fieldtype": "Date",
			"label": __("From Date"),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"fieldtype": "Date",
			"label": __("To Date"),
			"reqd": 1
		},
		{
			"fieldname": "academic_year",
			"fieldtype": "Data",
			"label": __("Academic Year"),
			"reqd": 1
		},
		{
			"fieldname": "company",
			"fieldtype": "Link",
			"label": __("Company"),
			"options": "Company",
			"reqd": 1
		},
		{
			"fieldname": "program",
			"fieldtype": "Link",
			"label": __("Program"),
			"options": "Program",
			"reqd": 1
		},
		// {
		// 	"fieldname": "studentwise_report",
		// 	"fieldtype": "Check",
		// 	"label": __("Studentwise Report"),
		// 	"reqd": 0
		// },
		{
			"fieldname": "summary_based_on_program",
			"fieldtype": "Check",
			"label": __("Summary Based on Program"),
			"reqd": 0
		},
		
		// {
		// 	"fieldname": "batchwise_report",
		// 	"fieldtype": "Check",
		// 	"label": __("Batchwise Report"),
		// 	"reqd": 0
		// }
	]
};


// "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),

// "default": frappe.datetime.get_today(),

// "default": "2021",