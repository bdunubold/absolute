from django.contrib import admin

# Register your models here.

from .models import Student, Class, Teacher, CourseType, Course, Contract

admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Teacher)
admin.site.register(CourseType)
admin.site.register(Course)
admin.site.register(Contract)
