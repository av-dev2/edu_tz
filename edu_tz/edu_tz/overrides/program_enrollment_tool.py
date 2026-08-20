import json
from typing import Any

import frappe
from frappe import _


@frappe.whitelist()
def enroll_all_students(self: Any):
	"""Enqueues enrollment when the batch is large, since the default tool times out on many students.

	:param self: Program Enrollment Tool
	"""
	self = frappe.get_doc(dict(json.loads(self)))

	if self.get_students_from == "Student Applicant":
		frappe.msgprint(_("Remove student applicants that are already created"))

	if len(self.students) > 30:
		frappe.enqueue("edu_tz.edu_tz.overrides.program_enrollment_tool.enroll_students", self=self)
		return "queued"

	enroll_students(self=self)
	return len(self.students)


@frappe.whitelist()
def enroll_students(self: Any):
	"""Copy of the ERPNext enrollment loop that also accepts a deserialised doc, so it can be enqueued.

	:param self: Program Enrollment Tool
	"""
	from education.education.api import enroll_student

	total = len(self.students)
	for index, student_row in enumerate(self.students):
		frappe.publish_realtime(
			"program_enrollment_tool",
			dict(progress=[index + 1, total]),
			user=frappe.session.user,
		)
		if student_row.student:
			program_enrollment = frappe.new_doc("Program Enrollment")
			program_enrollment.student = student_row.student
			program_enrollment.student_name = student_row.student_name
			program_enrollment.program = self.new_program
			program_enrollment.academic_year = self.new_academic_year
			program_enrollment.academic_term = self.new_academic_term
			program_enrollment.student_batch_name = student_row.student_batch_name or self.new_student_batch
			program_enrollment.save()
		elif student_row.student_applicant:
			program_enrollment = enroll_student(student_row.student_applicant)
			program_enrollment.academic_year = self.academic_year
			program_enrollment.academic_term = self.academic_term
			program_enrollment.student_batch_name = student_row.student_batch_name or self.new_student_batch
			program_enrollment.save()
