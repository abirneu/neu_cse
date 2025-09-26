from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from cse_app.models import FacultyMember


class Command(BaseCommand):
    help = 'Link a specific faculty member to a user account'

    def add_arguments(self, parser):
        parser.add_argument('--faculty-id', type=int, required=True, help='ID of faculty member')
        parser.add_argument('--user-id', type=int, help='ID of user to link')
        parser.add_argument('--username', type=str, help='Username of user to link')

    def handle(self, *args, **options):
        faculty_id = options['faculty_id']
        user_id = options.get('user_id')
        username = options.get('username')

        try:
            faculty = FacultyMember.objects.get(id=faculty_id)
        except FacultyMember.DoesNotExist:
            raise CommandError(f'Faculty member with ID {faculty_id} does not exist.')

        # Get user
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise CommandError(f'User with ID {user_id} does not exist.')
        elif username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise CommandError(f'User with username "{username}" does not exist.')
        else:
            raise CommandError('You must provide either --user-id or --username')

        # Check if user is already linked
        if hasattr(user, 'facultymember'):
            raise CommandError(f'User "{user.username}" is already linked to faculty member "{user.facultymember.name}"')

        # Link them
        faculty.user = user
        faculty.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully linked faculty member "{faculty.name}" to user "{user.username}"'
            )
        )