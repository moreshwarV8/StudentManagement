from django.contrib import admin
from .models import User, Department, Student, Attendance, StudentActivity

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']
    search_fields = ['username', 'email']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'name', 'department', 'semester', 'email']
    list_filter = ['department', 'semester', 'gender']
    search_fields = ['roll_number', 'name', 'email']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'present']
    list_filter = ['date', 'present']
    search_fields = ['student__name', 'student__roll_number']

@admin.register(StudentActivity)
class StudentActivityAdmin(admin.ModelAdmin):
    list_display = ['student', 'action', 'timestamp']
    list_filter = ['action']
    search_fields = ['student__name', 'student__roll_number']
    readonly_fields = ['timestamp']
