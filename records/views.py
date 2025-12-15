from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views

from .models import Student, Enrollment, Mark, Module, Lecturer
from django.db.models import Q
from .forms import StudentRegistrationForm, LecturerRegistrationForm
from django.contrib import messages
def register(request):
	if request.method == 'POST':
		form = StudentRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Registration successful! You can now log in.')
			return redirect('/accounts/login/')
	else:
		form = StudentRegistrationForm()
	return render(request, 'registration/register.html', {'form': form})
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

@login_required
def download_transcript_pdf(request, student_id):
	student = get_object_or_404(Student, id=student_id)
	if not request.user.is_staff:
		if not hasattr(request.user, 'student') or request.user.student.id != student.id:
			return HttpResponseForbidden("You are not allowed to download this transcript.")
	enrollments = Enrollment.objects.filter(student=student).order_by('academic_year', 'semester')
	results = []
	for enrollment in enrollments:
		mark = Mark.objects.filter(enrollment=enrollment).first()
		results.append({
			'module': enrollment.module,
			'year': enrollment.academic_year,
			'semester': enrollment.semester,
			'mark': mark.mark if mark else None
		})
	context = {
		'student': student,
		'results': results
	}
	template = get_template('records/full_transcript.html')
	html = template.render(context)
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = f'attachment; filename="transcript_{student.student_number}.pdf"'
	pisa_status = pisa.CreatePDF(html, dest=response)
	if pisa_status.err:
		return HttpResponse('We had some errors with PDF generation')
	return response

@login_required
def my_transcript_redirect(request):
	if request.user.is_staff:
		return redirect('homepage')
	if hasattr(request.user, 'student'):
		return redirect('full_transcript', student_id=request.user.student.id)
	return HttpResponseForbidden("No student record linked to this user.")

def homepage(request):
	students = Student.objects.all()
	q = request.GET.get('q', '').strip()
	if q:
		students = students.filter(
			Q(first_name__icontains=q) |
			Q(last_name__icontains=q) |
			Q(student_number__icontains=q)
		)
	context = {'students': students}
	return render(request, 'records/homepage.html', context)

@login_required
def semester_result_slip(request, student_id, year, semester):
	student = get_object_or_404(Student, id=student_id)
	# Only allow the student or staff to view
	if not request.user.is_staff:
		if not hasattr(request.user, 'student') or request.user.student.id != student.id:
			return HttpResponseForbidden("You are not allowed to view this result slip.")
	enrollments = Enrollment.objects.filter(student=student, academic_year=year, semester=semester)
	results = []
	for enrollment in enrollments:
		mark = Mark.objects.filter(enrollment=enrollment).first()
		results.append({
			'module': enrollment.module,
			'mark': mark.mark if mark else None
		})
	context = {
		'student': student,
		'year': year,
		'semester': semester,
		'results': results
	}
	return render(request, 'records/semester_result_slip.html', context)

@login_required
def academic_record(request, student_id, year):
	student = get_object_or_404(Student, id=student_id)
	if not request.user.is_staff:
		if not hasattr(request.user, 'student') or request.user.student.id != student.id:
			return HttpResponseForbidden("You are not allowed to view this academic record.")
	enrollments = Enrollment.objects.filter(student=student, academic_year=year)
	results = []
	for enrollment in enrollments:
		mark = Mark.objects.filter(enrollment=enrollment).first()
		results.append({
			'module': enrollment.module,
			'semester': enrollment.semester,
			'mark': mark.mark if mark else None
		})
	context = {
		'student': student,
		'year': year,
		'results': results
	}
	return render(request, 'records/academic_record.html', context)

@login_required
def full_transcript(request, student_id):
	student = get_object_or_404(Student, id=student_id)
	if not request.user.is_staff:
		if not hasattr(request.user, 'student') or request.user.student.id != student.id:
			return HttpResponseForbidden("You are not allowed to view this transcript.")
	enrollments = Enrollment.objects.filter(student=student).order_by('academic_year', 'semester')
	results = []
	total_credits = 0
	total_marks = 0
	mark_count = 0
	distinctions = 0
	fails = 0
	for enrollment in enrollments:
		mark = Mark.objects.filter(enrollment=enrollment).first()
		mark_value = float(mark.mark) if mark else None
		# Determine status
		if mark_value is None:
			status = "N/A"
		elif mark_value >= 75:
			status = "Distinction"
			distinctions += 1
		elif mark_value <= 45:
			status = "Fail"
			fails += 1
		elif 46 <= mark_value <= 49:
			status = "Fail (Supplementary Allowed)"
			fails += 1
		else:
			status = "Pass"
		if mark_value is not None:
			total_marks += mark_value
			mark_count += 1
			total_credits += enrollment.module.credit_hours
		results.append({
			'module': enrollment.module,
			'year': enrollment.academic_year,
			'semester': enrollment.semester,
			'mark': mark.mark if mark else None,
			'status': status
		})
	average_mark = round(total_marks / mark_count, 2) if mark_count else None
	gpa = round(total_marks / mark_count / 25, 2) if mark_count else None  # Example: scale GPA to 4.0
	context = {
		'student': student,
		'results': results,
		'total_credits': total_credits,
		'average_mark': average_mark,
		'distinctions': distinctions,
		'fails': fails,
		'gpa': gpa,
	}
	return render(request, 'records/full_transcript.html', context)

@login_required
def register_lecturer(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only admins can register lecturers.")
    if request.method == 'POST':
        form = LecturerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lecturer registered successfully!')
            return redirect('/admin/')
    else:
        form = LecturerRegistrationForm()
    return render(request, 'registration/register_lecturer.html', {'form': form})

def is_lecturer(user):
    return user.is_authenticated and user.is_staff and hasattr(user, 'lecturer')

from django.contrib.auth import get_user_model

def is_academic_lecturer(user):
    return user.is_authenticated and not user.is_superuser and user.is_staff and hasattr(user, 'lecturer')

@user_passes_test(is_academic_lecturer)
def lecturer_dashboard(request):
    modules = Module.objects.filter(lecturer=request.user)
    return render(request, 'lecturer/dashboard.html', {'modules': modules})

@user_passes_test(is_academic_lecturer)
def lecturer_module_students(request, module_id):
    module = get_object_or_404(Module, id=module_id, lecturer=request.user)
    enrollments = Enrollment.objects.filter(module=module).select_related('student')
    if request.method == 'POST':
        for enrollment in enrollments:
            mark_val = request.POST.get(f'mark_{enrollment.id}')
            if mark_val is not None and mark_val != '':
                mark_obj, created = Mark.objects.get_or_create(enrollment=enrollment)
                mark_obj.mark = mark_val
                mark_obj.save()
        messages.success(request, 'Marks updated successfully!')
        return redirect('lecturer_module_students', module_id=module.id)
    for enrollment in enrollments:
        enrollment.mark = getattr(enrollment, 'mark', None) or Mark.objects.filter(enrollment=enrollment).first()
    return render(request, 'lecturer/edit_marks.html', {'module': module, 'enrollments': enrollments})

class LecturerLoginView(auth_views.LoginView):
    template_name = 'lecturer/login.html'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('lecturer_dashboard')
