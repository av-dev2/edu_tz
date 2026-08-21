from typing import Any

import frappe
from education.education.doctype.program_enrollment.program_enrollment import ProgramEnrollment
from frappe import _


class EduTzProgramEnrollment(ProgramEnrollment):
	def create_course_enrollments(self):
		"""Enrolls the student in every course of the program, not only the courses listed on the enrollment."""
		student = frappe.get_doc("Student", self.student)
		program = frappe.get_doc("Program", self.program)
		for course in program.courses:
			student.enroll_in_course(course_name=course.course, program_enrollment=self.name)


def validate_submit_program_enrollment(doc: Any, method: Any = None):
	if not doc.student_category:
		frappe.throw(_("Please set Student Category"))


@frappe.whitelist()
def get_fee_schedule(
	program: str, academic_year: str, academic_term: str | None = None, student_category: str | None = None
):
	"""Returns the Program Fee rows whose Fee Structure matches the academic year and term."""
	program_fees = frappe.get_list(
		"Program Fee",
		fields=["academic_term", "fee_structure", "due_date", "amount"],
		filters={"parent": program, "student_category": student_category},
		parent_doctype="Program Enrollment",
		order_by="idx",
	)

	fees_list = []
	for fee in program_fees:
		fee_structure_year, fee_structure_term = frappe.get_value(
			"Fee Structure", fee["fee_structure"], ["academic_year", "academic_term"]
		)
		if fee_structure_year != academic_year:
			continue
		if academic_term and fee_structure_term != academic_term:
			continue
		fees_list.append(fee)

	return fees_list
