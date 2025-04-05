from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Student, Department, Attendance, StudentActivity
from .forms import StudentForm, AttendanceForm, UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'students/register.html', {'form': form})

@login_required
def home(request):
    total_students = Student.objects.count()
    total_departments = Department.objects.count()
    context = {
        'total_students': total_students,
        'total_departments': total_departments,
    }
    return render(request, 'students/home.html', context)

@login_required
def student_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        students = Student.objects.filter(
            Q(roll_number__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(department__name__icontains=search_query)
        )
    else:
        students = Student.objects.all()
    return render(request, 'students/student_list.html', {'students': students})

@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            StudentActivity.objects.create(student=student, action='Student Created')
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Add Student'})

@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            StudentActivity.objects.create(student=student, action='Student Updated')
            messages.success(request, 'Student updated successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Edit Student'})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        StudentActivity.objects.create(student=student, action='Student Deleted')
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})

@login_required
def attendance_list(request):
    attendances = Attendance.objects.all().order_by('-date')
    return render(request, 'students/attendance_list.html', {'attendances': attendances})

@login_required
def attendance_create(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance marked successfully!')
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'students/attendance_form.html', {'form': form})

@login_required
def student_activity_list(request):
    activities = StudentActivity.objects.all().order_by('-timestamp')
    return render(request, 'students/activity_list.html', {'activities': activities})
