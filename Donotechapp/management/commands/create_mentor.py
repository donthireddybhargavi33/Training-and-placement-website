from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Donotechapp.models import UserProfile, Mentor

class Command(BaseCommand):
    help = 'Create a mentor superuser with MENTOR role'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username for the mentor')
        parser.add_argument('email', type=str, help='Email for the mentor')
        parser.add_argument('password', type=str, help='Password for the mentor')
        parser.add_argument('--full_name', type=str, default='Mentor User', help='Full name of the mentor')
        parser.add_argument('--phone_number', type=str, default='0000000000', help='Phone number of the mentor')
        parser.add_argument('--bio', type=str, default='', help='Bio of the mentor')
        parser.add_argument('--company', type=str, default='', help='Company of the mentor')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        email = kwargs['email']
        password = kwargs['password']
        full_name = kwargs['full_name']
        phone_number = kwargs['phone_number']
        bio = kwargs['bio']
        company = kwargs['company']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f"User '{username}' already exists."))
            return

        user = User.objects.create_user(username=username, email=email, password=password, is_staff=False, is_superuser=False)
        UserProfile.objects.create(user=user, role='MENTOR')
        mentor = Mentor.objects.create(
            user=user,
            username=username,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            bio=bio,
            company=company
        )
        mentor.save()
        self.stdout.write(self.style.SUCCESS(f"Mentor user '{username}' created successfully with MENTOR role."))


