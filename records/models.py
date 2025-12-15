
from django.db import models
from django.contrib.auth.models import User

# Lecturer model for storing lecturer details
class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    staff_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    office = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.staff_number} - {self.first_name} {self.last_name}"


from django.db import models
from django.contrib.auth.models import User

class Programme(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	duration_years = models.PositiveIntegerField(default=3)

	def __str__(self):
		return self.name

class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	student_number = models.CharField(max_length=20, unique=True)
	programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
	enrollment_year = models.PositiveIntegerField()

	def __str__(self):
		return f"{self.student_number} - {self.first_name} {self.last_name}"


class Module(models.Model):
	code = models.CharField(max_length=10, unique=True)
	name = models.CharField(max_length=100)
	description = models.TextField()
	credit_hours = models.PositiveIntegerField()
	programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
	semester = models.PositiveIntegerField()
	lecturer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'is_staff': True}, related_name='modules_taught')

	def __str__(self):
		return f"{self.code} - {self.name}"

class Enrollment(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	module = models.ForeignKey(Module, on_delete=models.CASCADE)
	academic_year = models.PositiveIntegerField()
	semester = models.PositiveIntegerField()

	class Meta:
		unique_together = ("student", "module", "academic_year", "semester")

	def __str__(self):
		return f"{self.student} enrolled in {self.module} ({self.academic_year} S{self.semester})"

class Mark(models.Model):
	enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE)
	mark = models.DecimalField(max_digits=5, decimal_places=2)

	def __str__(self):
		return f"{self.enrollment}: {self.mark}"
