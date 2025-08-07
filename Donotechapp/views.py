from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Year, CourseItem, Student
from .forms import CourseForm
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def mycourses(request):
    student = get_object_or_404(Student, user=request.user)
    courses = student.courses_registered.all().select_related('semester__year')
    return render(request, 'my_courses.html', {'courses': courses})
    
def programs(request):
    return render(request, 'programs.html')

def internship(request):
    return render(request, 'internship.html')

def courses(request):
    years = Year.objects.prefetch_related('semesters__course_items').all().order_by('number')
    context = {
        'years': years,
    }
    return render(request, 'courses.html', context)

def jobs(request):
    return render(request, 'jobs.html')

def projects(request):
    return render(request, 'projects.html')

def strategy(request):
    return render(request, 'strategy.html')

def about(request):
    return render(request, 'about.html')

@staff_member_required
def course_detail(request, pk):
    course = get_object_or_404(CourseItem, pk=pk)
    return render(request, 'course_detail.html', {'course': course})


@staff_member_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, 'Course created successfully!')
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'course_form.html', {'form': form})

@staff_member_required
def course_update(request, pk):
    course = get_object_or_404(CourseItem, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    return render(request, 'course_form.html', {'form': form})

@staff_member_required
def course_delete(request, pk):
    course = get_object_or_404(CourseItem, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('courses')
    return render(request, 'course_confirm_delete.html', {'course': course})


from .forms import (
    StudentRegistrationForm,
    StudentForm
)


from django.contrib.auth.decorators import login_required
import logging
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render
from .models import TieUp
from django.core.mail import send_mail
from django.conf import settings




def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        if not name or not email or not message:
            messages.error(request, 'All fields are required.')
        else:
            # Send email to admin
            subject = f"New Contact Form Submission from {name}"
            message_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            admin_email = getattr(settings, 'ADMIN_EMAIL', None)
            if admin_email:
                try:
                    send_mail(
                        subject,
                        message_body,
                        settings.EMAIL_HOST_USER,
                        [admin_email],
                        fail_silently=False,
                        # reply_to argument removed due to Django version compatibility
                    )
                except Exception as e:
                    messages.error(request, f"An error occurred while sending your message: {e}")
                    return render(request, 'contact.html')
            messages.success(request, 'Thank you for your message. We will get back to you soon.')
            return redirect('contact')
    return render(request, 'contact.html')

def home(request):
    context = {
        'institution_name': "DONOTECH SOLUTIONS",
        'institution_details': "DONOTECH SOLUTIONS is a premier placement and training institute dedicated to bridging the gap between academia and industry. We provide cutting-edge training programs and placement assistance to help students launch successful careers in technology.",
        
        'tieups': TieUp.objects.all(),
      
        # 'experiences': StudentExperience.objects.all(),
    }
    return render(request, 'home.html', context)

logger = logging.getLogger(__name__)

from .models import UserProfile

from .forms import StudentRegistrationForm

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                # Create UserProfile
                UserProfile.objects.create(user=user, role='STUDENT')
                # Create Student profile
                student = form.save(commit=False)
                student.user = user
                student.save()
                form.save_m2m()
                messages.success(request, 'Registration successful! You can log in now.')
                return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        role = request.POST.get('role', '').strip()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            from .models import Student, Mentor
            # Try to get or create UserProfile
            profile, created = UserProfile.objects.get_or_create(user=user, defaults={'role': role})
            if not created and profile.role != role:
                messages.error(request, f"Your account role is '{profile.role}', but you selected '{role}'.")
                return render(request, 'login.html')
            # Validate extra fields for student role and create missing profile if needed
            if role == 'STUDENT':
                student, s_created = Student.objects.get_or_create(user=user)
            elif role == 'MENTOR':
                mentor, m_created = Mentor.objects.get_or_create(user=user)
            login(request, user)
            # Redirect to respective dashboards
            if role == 'STUDENT':
                return redirect('student_dashboard')
            elif role == 'MENTOR':
                return redirect('mentor_dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# Separate dashboards for each role
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


from django.http import HttpResponseForbidden

def role_required(role):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            try:
                profile = UserProfile.objects.get(user=request.user)
                if profile.role == role:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden('You are not authorized to view this page.')
            except UserProfile.DoesNotExist:
                return HttpResponseForbidden('User profile not found.')
        return _wrapped_view
    return decorator




from django.shortcuts import get_object_or_404
from django.http import JsonResponse

@role_required('STUDENT')
def student_dashboard(request):
    from .models import Student, CourseProgress
    student_profile = None
    courses_with_progress = []
    completed_courses_count = 0
    mentor = None
    
    try:
        student_profile = Student.objects.get(user=request.user)
        mentor = student_profile.mentor
        
        # Get courses with progress
        registered_courses = student_profile.courses_registered.all()
        for course in registered_courses:
            progress, created = CourseProgress.objects.get_or_create(
                student=student_profile,
                course=course,
                defaults={'progress': 0}
            )
            courses_with_progress.append({
                'course': course,
                'progress': progress.progress,
                'id': progress.id  # Add progress record ID for editing
            })
            if progress.progress == 100:
                completed_courses_count += 1
                
    except Student.DoesNotExist:
        pass
        
    return render(request, 'student_dashboard.html', {
        'student_profile': student_profile,
        'courses_with_progress': courses_with_progress,
        'completed_courses_count': completed_courses_count,
        'mentor': mentor
    })

@login_required
def update_course_progress(request):
    if request.method == 'POST':
        progress_id = request.POST.get('progress_id')
        new_progress = request.POST.get('progress')
        
        try:
            progress = get_object_or_404(CourseProgress, id=progress_id)
            if progress.student.user != request.user:
                return JsonResponse({'success': False, 'error': 'Unauthorized'})
                
            progress.progress = min(100, max(0, int(new_progress)))
            progress.save()
            return JsonResponse({'success': True, 'new_progress': progress.progress})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})
# Student details page for admin or staff
from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required
def student_details(request):
    from .models import Student
    students = Student.objects.all()
    return render(request, 'student_details.html', {'students': students})

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Student
from .forms import StudentForm
from django.contrib import messages
from django.shortcuts import render

def about_us(request):
    return render(request, 'about_us.html')

@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, 'Student created successfully!')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form})

@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_form.html', {'form': form})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_details')
    return render(request, 'student_confirm_delete.html', {'student': student})

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
import json

def gen_resume(request):
    if request.method == "POST":
        # Process form data
        data = {
            "name": request.POST.get("name", ""),
            "email": request.POST.get("email", ""),
            "linkedin": request.POST.get("linkedin", ""),
            "phone": request.POST.get("phone", ""),
            "summary": request.POST.get("summary", ""),
            "skills": [skill for skill in request.POST.getlist("skills") if skill],
            "work_experience": [],
            "education": [],
            "projects": [],
            "leadership": [item for item in request.POST.getlist("leadership") if item],
            "achievements": [item for item in request.POST.getlist("achievements") if item],
            "personal": {
                "father_name": request.POST.get("father_name", ""),
                "dob": request.POST.get("dob", ""),
                "gender": request.POST.get("gender", ""),
                "languages": request.POST.get("languages", ""),
                "marital_status": request.POST.get("marital_status", ""),
                "address": request.POST.get("address", ""),
            },

        }

        # Process dynamic work experience fields
        i = 1
        while True:
            role = request.POST.get(f"work_role{i}", "")
            if not role:
                break
            data["work_experience"].append({
                "role": role,
                "company": request.POST.get(f"work_company{i}", ""),
                "period": request.POST.get(f"work_period{i}", ""),
                "details": request.POST.get(f"work_details{i}", ""),
            })
            i += 1
        
        # Process dynamic education fields
        i = 1
        while True:
            name = request.POST.get(f"edu_name{i}", "")
            if not name:
                break
            data["education"].append({
                "name": name,
                "period": request.POST.get(f"edu_period{i}", ""),
                "details": request.POST.get(f"edu_details{i}", ""),
            })
            i += 1
        
        # Process dynamic project fields
        i = 1
        while True:
            title = request.POST.get(f"proj_title{i}", "")
            if not title:
                break
            data["projects"].append({
                "title": title,
                "year": request.POST.get(f"proj_year{i}", ""),
                "description": request.POST.get(f"proj_description{i}", ""),
            })
            i += 1
        
        # Save form data in session
        request.session['resume_form_data'] = json.dumps(data)
        
        # Check if user wants PDF download
        if "download" in request.POST:
            html_string = render_to_string("gen_resume.html", data)
            response = HttpResponse(content_type="application/pdf")
            response['Content-Disposition'] = f'attachment; filename="{data["name"].replace(" ", "_")}_Resume.pdf"'
            weasyprint.HTML(string=html_string).write_pdf(response)
            return response
        
        return render(request, 'gen_resume.html', data)
    
    # If GET request, check for saved form data
    saved_data = request.session.get('resume_form_data', None)
    if saved_data:
        try:
            form_data = json.loads(saved_data)
            return render(request, 'resume_form.html', {'form_data': form_data})
        except json.JSONDecodeError:
            pass
    
    return render(request, 'resume_form.html')


from django.shortcuts import render

def resume_form(request):
    return render(request, 'resume_form.html')