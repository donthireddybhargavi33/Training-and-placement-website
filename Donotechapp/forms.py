from django import forms
from .models import Student, CourseItem, Mentor

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(max_length=150, required=True, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')
    YEAR_SEMESTER_CHOICES = [
        (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8')
    ]
    year_semester = forms.ChoiceField(choices=[
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')
    ], required=True, label="Semester")
    courses_registered = forms.ModelMultipleChoiceField(
    queryset=CourseItem.objects.all(),
    required=False,
    widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    label="Courses Registered"
    )

    from .models import Mentor
    mentor = forms.ModelChoiceField(queryset=Mentor.objects.all(), required=False, empty_label="Select Mentor")
    class Meta:
        model = Student
        fields = [
            'username', 'email', 'phone_number', 'gender', 'date_of_birth',
            'college', 'courses_registered', 'department', 'year_semester', 'profile_image', 'mentor'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class StudentForm(forms.ModelForm):
    courses_registered = forms.ModelMultipleChoiceField(
        queryset=CourseItem.objects.all(),
        required=False,
        widget=forms.SelectMultiple,
        label="Courses Registered"
    )
    class Meta:
        model = Student
        fields = [
            'username', 'full_name', 'email', 'phone_number', 'gender', 
            'date_of_birth', 'college', 'courses_registered', 'department',
            'year_semester',  'profile_image'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'year_semester': forms.Select(choices=Student.YEAR_SEMESTER_CHOICES)
        }

class MentorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(max_length=150, required=True, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')
    class Meta:
        model = Mentor
        fields = [
            'username', 'full_name', 'email', 'phone_number',  'profile_image'
        ]

class CourseForm(forms.ModelForm):
    class Meta:
        model = CourseItem
        fields = ['semester', 'title', 'description', 'tools']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'tools': forms.Textarea(attrs={'rows': 2}),
        }


