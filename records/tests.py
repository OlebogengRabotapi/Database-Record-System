
from django.test import TestCase
from .models import Programme, Student, Module, Enrollment, Mark

class RecordsModelTests(TestCase):
	def setUp(self):
		self.programme = Programme.objects.create(name="BSc Computer Science", description="3-year CS programme", duration_years=3)
		self.student = Student.objects.create(first_name="John", last_name="Doe", student_number="SPU12345", programme=self.programme, enrollment_year=2023)
		self.module = Module.objects.create(code="CS101", name="Intro to CS", description="Basics of CS", credit_hours=16, programme=self.programme, semester=1)
		self.enrollment = Enrollment.objects.create(student=self.student, module=self.module, academic_year=2023, semester=1)
		self.mark = Mark.objects.create(enrollment=self.enrollment, mark=75.5)

	def test_programme_creation(self):
		self.assertEqual(self.programme.name, "BSc Computer Science")

	def test_student_creation(self):
		self.assertEqual(self.student.first_name, "John")
		self.assertEqual(self.student.programme, self.programme)

	def test_module_creation(self):
		self.assertEqual(self.module.code, "CS101")
		self.assertEqual(self.module.programme, self.programme)

	def test_enrollment_creation(self):
		self.assertEqual(self.enrollment.student, self.student)
		self.assertEqual(self.enrollment.module, self.module)

	def test_mark_creation(self):
		self.assertEqual(self.mark.enrollment, self.enrollment)
		self.assertEqual(float(self.mark.mark), 75.5)
