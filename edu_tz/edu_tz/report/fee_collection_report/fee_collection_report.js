// Copyright (c) 2016, Aakvatech and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Fee Collection Report"] = {
	"filters": [
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
			"reqd": 0
		},
		{
			"fieldname": "summary_based_on_month",
			"fieldtype": "Check",
			"label": __("Summary Based on Month"),
			"reqd": 0
		}
	]
};