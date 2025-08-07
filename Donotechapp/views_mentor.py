from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from .models import Mentor, Student

@login_required
def mentor_dashboard(request):
    mentor_profile = None
    students = []
    upcoming_sessions = []
    pending_tasks = 0
    
    try:
        mentor_profile = Mentor.objects.get(user=request.user)
        students = Student.objects.filter(mentor=mentor_profile)
        
    except Mentor.DoesNotExist:
        pass
        
    return render(request, 'mentor_dashboard.html', {
        'mentor_profile': mentor_profile,
        'students': students
    })

@login_required
def mentor_student_details(request):
    mentor_profile = None
    students = []
    try:
        mentor_profile = Mentor.objects.get(user=request.user)
        students = Student.objects.filter(mentor=mentor_profile)[:20]
    except Mentor.DoesNotExist:
        pass
    return render(request, 'student_details.html', {
        'students': students, 
        'is_mentor_view': True
    })
