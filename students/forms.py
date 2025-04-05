from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Attendance, User

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_number', 'name', 'semester', 'gender', 'department', 'email', 'phone', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'present']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
