from django.contrib import admin

from .models import Programme, Student, Module, Enrollment, Mark, Lecturer
class LecturerAdmin(admin.ModelAdmin):
	list_display = ('staff_number', 'first_name', 'last_name', 'email', 'department', 'phone', 'office')
	search_fields = ('staff_number', 'first_name', 'last_name', 'email', 'department')



class ModuleAdmin(admin.ModelAdmin):
	exclude = ('description',)
	list_display = ('code', 'name', 'programme', 'semester', 'lecturer')
	list_select_related = ('lecturer',)
	search_fields = ('code', 'name', 'lecturer__username', 'lecturer__first_name', 'lecturer__last_name')

class ProgrammeAdmin(admin.ModelAdmin):
	exclude = ('description',)

admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(Student)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lecturer, LecturerAdmin)
class EnrollmentAdmin(admin.ModelAdmin):
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'module':
			if request._obj_ is not None:
				student = request._obj_.student
				kwargs["queryset"] = Module.objects.filter(programme=student.programme)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

	def get_form(self, request, obj=None, **kwargs):
		request._obj_ = obj
		return super().get_form(request, obj, **kwargs)

admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Mark)
