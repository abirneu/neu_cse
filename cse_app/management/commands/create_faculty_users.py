from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from cse_app.models import FacultyMember
import re

class Command(BaseCommand):
    help = 'Create user accounts for faculty members'

    def add_arguments(self, parser):
        parser.add_argument(
            '--faculty-id',
            type=int,
            help='Create user for specific faculty member by ID'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Create users for all faculty members without accounts'
        )
        parser.add_argument(
            '--list',
            action='store_true',
            help='List all faculty members and their user status'
        )

    def handle(self, *args, **options):
        if options['list']:
            self.list_faculty()
        elif options['all']:
            self.create_all_faculty_users()
        elif options['faculty_id']:
            self.create_faculty_user(options['faculty_id'])
        else:
            self.stdout.write(self.style.ERROR('Please provide an option: --list, --all, or --faculty-id'))

    def list_faculty(self):
        faculty_members = FacultyMember.objects.all().order_by('id')
        
        self.stdout.write(self.style.SUCCESS('\nFaculty Members Status:'))
        self.stdout.write('-' * 80)
        
        for faculty in faculty_members:
            status = '✓ Has User' if faculty.user else '✗ No User'
            username = f'({faculty.user.username})' if faculty.user else ''
            
            self.stdout.write(
                f'ID: {faculty.id:2d} | {faculty.name:30s} | {status:10s} {username}'
            )
        
        total_count = faculty_members.count()
        with_users = faculty_members.filter(user__isnull=False).count()
        without_users = total_count - with_users
        
        self.stdout.write('-' * 80)
        self.stdout.write(f'Total Faculty: {total_count}, With Users: {with_users}, Without Users: {without_users}')

    def create_all_faculty_users(self):
        faculty_without_users = FacultyMember.objects.filter(user__isnull=True)
        
        if not faculty_without_users.exists():
            self.stdout.write(self.style.WARNING('All faculty members already have user accounts.'))
            return
        
        self.stdout.write(f'Creating user accounts for {faculty_without_users.count()} faculty members...\n')
        
        for faculty in faculty_without_users:
            try:
                self.create_user_for_faculty(faculty)
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created user for {faculty.name}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Failed to create user for {faculty.name}: {str(e)}')
                )

    def create_faculty_user(self, faculty_id):
        try:
            faculty = FacultyMember.objects.get(id=faculty_id)
        except FacultyMember.DoesNotExist:
            raise CommandError(f'Faculty member with ID {faculty_id} does not exist.')
        
        if faculty.user:
            self.stdout.write(
                self.style.WARNING(f'{faculty.name} already has a user account: {faculty.user.username}')
            )
            return
        
        try:
            user = self.create_user_for_faculty(faculty)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created user account for {faculty.name}')
            )
            self.stdout.write(f'Username: {user.username}')
            self.stdout.write(f'Password: faculty123 (change this after first login)')
        except Exception as e:
            raise CommandError(f'Failed to create user for {faculty.name}: {str(e)}')

    def create_user_for_faculty(self, faculty):
        """Create a user account for a faculty member"""
        # Generate username from name (remove special characters, convert to lowercase)
        name_parts = re.sub(r'[^a-zA-Z\s]', '', faculty.name).split()
        
        # Create username: first name + first letter of other names
        if len(name_parts) >= 2:
            username = name_parts[0].lower() + ''.join([part[0].lower() for part in name_parts[1:]])
        else:
            username = name_parts[0].lower() if name_parts else f'faculty{faculty.id}'
        
        # Ensure username is unique
        original_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f'{original_username}{counter}'
            counter += 1
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=faculty.email,
            password='faculty123',  # Default password
            first_name=faculty.name.split()[0] if faculty.name else '',
            last_name=' '.join(faculty.name.split()[1:]) if len(faculty.name.split()) > 1 else ''
        )
        
        # Link user to faculty
        faculty.user = user
        faculty.save()
        
        return user