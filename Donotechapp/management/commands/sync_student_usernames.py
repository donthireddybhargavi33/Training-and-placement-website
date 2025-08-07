from django.core.management.base import BaseCommand
from Donotechapp.models import Student
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Sync Student.username with User.username for all students.'

    def handle(self, *args, **options):
        updated = 0
        for student in Student.objects.all():
            if student.username and student.user.username != student.username:
                user = student.user
                user.username = student.username
                user.save()
                updated += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully synced usernames for {updated} students.'))
