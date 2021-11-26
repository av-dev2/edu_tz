import frappe
from frappe import _

def execute(filters=None):
	data = []
	columns = get_columns(filters)

	fee_data = get_fees(filters)
	if fee_data:
		data += fee_data

	summary_based = get_summary_based_on_program(filters)
	# , chart
	if summary_based:
		data += summary_based

	return columns, data #None, chart

def get_columns(filters):

	if filters.summary_based_on_program:
		columns = [
			{"fieldname": "academic_year", "fieldtype": "Data", "label": _("Academic Year")},
			{"fieldname": "program", "fieldtype": "Data", "label": _("Program")},
			{"fieldname": "total_amount_to_be_paid", "fieldtype": "Currency", "label": _("Total Fee to be Collected")},
			{"fieldname": "total_paid_amount", "fieldtype": "Currency", "label": _("Total Fee Collected")},
			{"fieldname": "outstanding_amount", "fieldtype": "Currency", "label": _("Outstanding Amount")}
		]
	
	else:
		columns = [
			{"fieldname": "academic_year", "fieldtype": "Data", "label": _("Academic Year")},
			{"fieldname": "student_name", "fieldtype": "Data", "label": _("Student Name")},
			{"fieldname": "program", "fieldtype": "Data", "label": _("Program")},
			{"fieldname": "class_name", "fieldtype": "Data", "label": _("Class Name")},
			{"fieldname": "fee_category", "fieldtype": "Data", "label": _("Fee Category")},
			{"fieldname": "total_amount_to_be_paid", "fieldtype": "Currency", "label": _("Fee to be Collected")},
			{"fieldname": "first_installment_paid_amount", "fieldtype": "Currency", "label": _("1st Installment Paid")},
			{"fieldname": "second_installment_paid_amount", "fieldtype": "Currency", "label": _("2nd Installment Paid")},
			{"fieldname": "third_installment_paid_amount", "fieldtype": "Currency", "label":_("3rd Installment Paid")},
			{"fieldname": "fourth_installment_paid_amount", "fieldtype": "Currency", "label": _("4th Installment Paid")},
			{"fieldname": "total_paid_amount", "fieldtype": "Currency", "label": _("Total Fee Collected")},
			{"fieldname": "outstanding_amount", "fieldtype": "Currency", "label": _("Outstanding Amount")}
		]
	return columns

def get_fees(filters):
	data = []
	fees_records = []
	if not filters.summary_based_on_program:
		student_details, fee_details = get_fee_details(filters)

		first_installment_list = []
		second_installment_list = []
		third_installment_list = []
		fourth_installment_list = []

		for student in student_details:
			total_amount_to_be_paid = total_unpaid_amount = 0
			for fee in fee_details:
				if student["student"] == fee["student"]:
					total_amount_to_be_paid += fee.grand_total
					total_unpaid_amount += fee.outstanding_amount

					fee_category = fee["student_category"]
					program =  fee.program

					if student not in first_installment_list:
						student.update({
							"posting_date": fee.posting_date,
							"program": fee.program,
							"class_name": student["class_name"],
							"amount_to_be_paid": fee.grand_total,
							"paid_amount1": fee.grand_total - fee.outstanding_amount,
							"unpaid_amount": fee.outstanding_amount
						})
						first_installment_list.append(student)

					elif student not in second_installment_list:
						student.update({
							"posting_date": fee.posting_date,
							"program": fee.program,
							"class_name": student["class_name"],
							"amount_to_be_paid": fee.grand_total,
							"paid_amount2": fee.grand_total - fee.outstanding_amount,
							"unpaid_amount": fee.outstanding_amount
						})
						second_installment_list.append(student)

					elif student not in third_installment_list:
						student.update({
							"posting_date": fee.posting_date,
							"program": fee.program,
							"class_name": student["class_name"],
							"amount_to_be_paid": fee.grand_total,
							"paid_amount3": fee.grand_total - fee.outstanding_amount,
							"unpaid_amount": fee.outstanding_amount
						})
						third_installment_list.append(student)

					else:
						student.update({
							"posting_date": fee.posting_date,
							"program": fee.program,
							"class_name": student["class_name"],
							"amount_to_be_paid": fee.grand_total,
							"paid_amount4": fee.grand_total - fee.outstanding_amount,
							"unpaid_amount": fee.outstanding_amount
						})
						fourth_installment_list.append(student)

			fees_records.append({
				"posting_date": fee.posting_date,
				"academic_year": student["academic_year"],
				"student": student["student"],
				"student_name": student["student_name"],
				"program": program,
				"class_name": student["class_name"],
				"fee_category": fee_category,
				"total_amount_to_be_paid": total_amount_to_be_paid,
				"outstanding_amount": total_unpaid_amount
			})
		
		for record in fees_records:
			paid_amount = 0
			for first in first_installment_list:
				if (record["student"] == first["student"] and 
					record["program"] == first["program"] and 
					record["class_name"] == first["class_name"]
				):
					record.update({
						"first_installment_paid_amount": first["paid_amount1"],
					})
					paid_amount += first["paid_amount1"]

			for second in second_installment_list:
				if (record["student"] == second["student"] and 
					record["program"] == second["program"] and 
					record["class_name"] == second["class_name"]
				):
					record.update({
						"second_installment_paid_amount": second["paid_amount2"]
					})
					paid_amount += second["paid_amount2"]
			
			for third in third_installment_list:
				if (record["student"] == third["student"] and 
					record["program"] == third["program"] and 
					record["class_name"] == third["class_name"]
				):
					record.update({
						"third_installment_paid_amount": third["paid_amount3"]
					})
					paid_amount += third["paid_amount3"]
			
			for fourth in fourth_installment_list:
				if (record["student"] == fourth["student"] and 
					record["program"] == fourth["program"] and 
					record["class_name"] == fourth["class_name"]
				):
					record.update({
						"fourth_installment_paid_amount": fourth["paid_amount4"]
					})
					paid_amount += fourth["paid_amount4"]

			record["total_paid_amount"] = paid_amount
			data.append(record)
	return data

def get_filter_condtions(filters):
	conditions = ""
	if filters.get("program"):
		conditions += "AND fe.program = %(program)s"
		conditions += "AND p_en.program = %(program)s"
	if filters.get("company"):
		conditions += "AND fe.company = %(company)s"
	if filters.get("academic_year"):
		conditions += "AND fe.academic_year = %(academic_year)s"
		conditions += "AND p_en.academic_year = %(academic_year)s"
	if filters.get("from_date") and filters.get("to_date"):
		conditions += "AND fe.posting_date BETWEEN %(from_date)s AND %(to_date)s"

	return conditions

def get_fee_details(filters):
	conditions = get_filter_condtions(filters)
	student_details, student_list = get_student_groups(filters)

	student_list = tuple(student_list)

	fee_details = frappe.db.sql("""
		SELECT fe.posting_date, fe.student, fe.student_name, fe.program, 
			fe.grand_total, fe.outstanding_amount, p_en.student_category
			FROM `tabFees` fe
			INNER JOIN `tabProgram Enrollment` p_en ON fe.student = p_en.student
			WHERE fe.docstatus = 1
			AND fe.student IN {student_list} {conditions}
		ORDER BY fe.posting_date desc
	""".format(student_list=student_list, conditions=conditions), filters, as_dict=1)

	return student_details, fee_details

def get_student_groups(filters):
	students = []
	if not filters.summary_based_on_program:
		name_list = []

		if filters.get("program") and filters.get("academic_year"):
			conditions = " AND sg.program = %(program)s AND sg.academic_year = %(academic_year)s"

		st_groups = frappe.db.sql("""
			SELECT sg.name, sg.program, sg.academic_year, sgs.student, sgs.student_name
			FROM `tabStudent Group` sg
			INNER JOIN `tabStudent Group Student` sgs ON sg.name = sgs.parent
			WHERE sg.disabled = 0  AND sgs.active = 1 {conditions}
			ORDER BY sg.name""".format(conditions=conditions), filters, as_dict=1)
		
		for student in st_groups:
			if student.academic_year == 2020:
				program_class = student.name

			elif "FORM" or "TODDLERS" in student.name:
				p_txt = student.name
				ph, st = p_txt.split("-")
				program_class = st
			
			elif student.academic_year != 2020:
				txt = student.name
				year, pro, stream = txt.split("-")
				program_class = pro +' - '+ stream

			else:
				continue

			name_list.append(student.student)
			
			students.append({
				"academic_year": student.academic_year,
				"student": student.student,
				"student_name": student.student_name,
				"class_name": program_class,
			})
					
	return students, name_list

def get_summary_based_on_program(filters):
	if filters.summary_based_on_program:
		data = []

		program_fees = frappe.get_all(
			"Fees", filters=[["docstatus", "=", 1], ["company", "=", filters.get("company")],
				["program", "!=", ""], ["academic_year", "=", filters.get("academic_year")],
				["posting_date", "between", [filters.get("from_date"), filters.get("to_date")]]
			], fields=["program", "academic_year", "grand_total", "outstanding_amount"],
			order_by="program asc"
		)

		program_list = frappe.get_all("Program", "name")

		for program in program_list:
			total_paid_amount = total_unpaid_amount = total_amount_to_be_paid = 0

			for entry in program_fees:
				if program.name == entry.program:
					total_amount_to_be_paid += entry.grand_total
					total_unpaid_amount += entry.outstanding_amount

					diff_amount = entry.grand_total - entry.outstanding_amount
					total_paid_amount += diff_amount

				else:
					continue

			data.append({
				"academic_year": entry.academic_year,
				"program": program.name,
				"total_paid_amount": total_paid_amount,
				"outstanding_amount": total_unpaid_amount,
				"total_amount_to_be_paid": total_amount_to_be_paid
			})

		# chart = get_chart_data(data)
		
		return data #chart

def get_chart_data(summary_data):
	
	if not summary_data:
		return

	labels = []
	fees_collected = []
	outstanding_amount = []
	fees_to_be_collected = []

	for entry in summary_data:
		labels.append(entry.get('program'))
		fees_collected.append(entry.get('total_paid_amount'))
		outstanding_amount.append(entry.get('outstanding_amount'))
		fees_to_be_collected.append(entry.get('total_amount_to_be_paid'))

	return {
		'data': {
			'labels': labels,
			'datasets': [
				{
					'name': _('Fee to be Collected'),
					'values': fees_to_be_collected
				},
				{
					'name': _('Fees Collected'),
					'values': fees_collected
				},
				{
					'name': _('Outstanding Amount'),
					'values': outstanding_amount
				}
			]
		},
		'type': 'bar'
	}


