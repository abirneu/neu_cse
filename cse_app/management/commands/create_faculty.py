from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from cse_app.models import FacultyMember


class Command(BaseCommand):
    help = 'Create a new faculty member with associated user account'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, required=True, help='Username for the faculty')
        parser.add_argument('--password', type=str, required=True, help='Password for the faculty')
        parser.add_argument('--email', type=str, required=True, help='Email for the faculty')
        parser.add_argument('--name', type=str, required=True, help='Full name of the faculty')
        parser.add_argument('--designation', type=str, required=True, 
                          choices=['professor', 'associate_professor', 'assistant_professor', 'lecturer', 'chairman'],
                          help='Faculty designation')
        parser.add_argument('--phone', type=str, help='Phone number (optional)')
        parser.add_argument('--room_no', type=str, help='Room number (optional)')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']
        name = options['name']
        designation = options['designation']
        phone = options.get('phone', '')
        room_no = options.get('room_no', '')

        try:
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                raise CommandError(f'User with username "{username}" already exists.')

            if User.objects.filter(email=email).exists():
                raise CommandError(f'User with email "{email}" already exists.')

            # Create User
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=name.split(' ')[0] if ' ' in name else name,
                last_name=' '.join(name.split(' ')[1:]) if ' ' in name else ''
            )

            # Create Faculty Member
            faculty = FacultyMember.objects.create(
                user=user,
                name=name,
                designation=designation,
                status='active',
                member_type='full_time',
                email=email,
                phone=phone,
                room_no=room_no,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created faculty member: {faculty.name} (ID: {faculty.id})'
                )
            )

        except Exception as e:
            raise CommandError(f'Error creating faculty member: {str(e)}')