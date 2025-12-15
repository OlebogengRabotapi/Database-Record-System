from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import LecturerLoginView

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('my-transcript/', views.my_transcript_redirect, name='my_transcript_redirect'),
    path('student/<int:student_id>/semester/<int:year>/<int:semester>/', views.semester_result_slip, name='semester_result_slip'),
    path('student/<int:student_id>/year/<int:year>/', views.academic_record, name='academic_record'),
    path('student/<int:student_id>/transcript/', views.full_transcript, name='full_transcript'),
    path('student/<int:student_id>/transcript/download/', views.download_transcript_pdf, name='download_transcript_pdf'),
    path('register/', views.register, name='register'),
    path('register-lecturer/', views.register_lecturer, name='register_lecturer'),
    path('lecturer/dashboard/', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('lecturer/module/<int:module_id>/students/', views.lecturer_module_students, name='lecturer_module_students'),
    path('lecturer-login/', LecturerLoginView.as_view(), name='lecturer_login'),
]
