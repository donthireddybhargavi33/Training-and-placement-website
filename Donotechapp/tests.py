from django.test import TestCase
from django.contrib.auth.models import User
from .models import Student, CourseItem, Year, Semester

class StudentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.year = Year.objects.create(number=1)
        self.semester = Semester.objects.create(year=self.year, number=1)
        self.course_item = CourseItem.objects.create(semester=self.semester, title='Test Course', description='Test Description')

    def test_student_courses_registered(self):
        student = Student.objects.create(user=self.user, username='teststudent')
        student.courses_registered.add(self.course_item)
        student.save()
        self.assertIn(self.course_item, student.courses_registered.all())

# Create your tests here.
