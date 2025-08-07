from django.urls import path
from . import views
from . import views_mentor

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin-dashboard/', views.dashboard_view, name='admin_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('mentor-dashboard/', views_mentor.mentor_dashboard, name='mentor_dashboard'),
    path('mentor-student-details/', views_mentor.mentor_student_details, name='mentor_student_details'),
    path('student-details/', views.student_details, name='student_details'),
    path('student-details/<int:pk>/', views.student_details, name='student_details'),
    path('students/create/', views.student_create, name='student_create'),
    path('students/<int:pk>/update/', views.student_update, name='student_update'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('courses/', views.courses, name='courses'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:pk>/update/', views.course_update, name='course_update'),
    path('courses/<int:pk>/delete/', views.course_delete, name='course_delete'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('programs/', views.programs, name='programs'),
    path('internship/',views.internship,name='internship'),
    path('jobs/', views.jobs, name='jobs'),
    path('projects/', views.projects, name='projects'),
    path('strategy/', views.strategy, name='strategy'),
    path('my_courses/',views.mycourses, name='my_courses'),
    path('gen_resume/', views.gen_resume, name='gen_resume'),
    path('resume_form/',views.resume_form,name='resume_form'),

]  
