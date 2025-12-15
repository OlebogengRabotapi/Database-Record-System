from django import forms
from django.contrib.auth.models import User
from .models import Student, Lecturer

class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'student_number', 'programme', 'enrollment_year']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        student = super().save(commit=False)
        student.user = user
        if commit:
            student.save()
        return student

class LecturerRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Lecturer
        fields = ['first_name', 'last_name', 'email', 'staff_number', 'department', 'phone', 'office']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            is_staff=True
        )
        lecturer = super().save(commit=False)
        lecturer.user = user
        if commit:
            lecturer.save()
        return lecturer
