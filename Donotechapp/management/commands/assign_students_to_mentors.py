from django.core.management.base import BaseCommand
from Donotechapp.models import Mentor, Student

class Command(BaseCommand):
    help = 'Automatically assign 20 students to each mentor'

    def handle(self, *args, **kwargs):
        mentors = Mentor.objects.all()
        unassigned_students = Student.objects.filter(mentor__isnull=True)
        total_assigned = 0

        for mentor in mentors:
            assigned_count = Student.objects.filter(mentor=mentor).count()
            to_assign = 20 - assigned_count
            if to_assign > 0:
                students_to_assign = unassigned_students[:to_assign]
                for student in students_to_assign:
                    student.mentor = mentor
                    student.save()
                    total_assigned += 1
                unassigned_students = unassigned_students[to_assign:]

        self.stdout.write(self.style.SUCCESS(f"Assigned {total_assigned} students to mentors."))
