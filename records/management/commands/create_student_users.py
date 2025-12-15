from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from records.models import Student

class Command(BaseCommand):
    help = 'Create user accounts for students who do not have one and link them.'

    def handle(self, *args, **options):
        students = Student.objects.filter(user__isnull=True)
        for student in students:
            username = student.student_number.lower()
            password = User.objects.make_random_password()
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=student.first_name,
                last_name=student.last_name,
            )
            student.user = user
            student.save()
            self.stdout.write(self.style.SUCCESS(
                f'Created user {username} for student {student} with password: {password}'
            ))
