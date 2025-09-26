from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cse_app.models import FacultyMember


class Command(BaseCommand):
    help = 'Show status of users and faculty member linkings'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n=== USER AND FACULTY LINKING STATUS ===\n'))
        
        # Show all users
        all_users = User.objects.all().order_by('username')
        self.stdout.write(f"Total Users: {all_users.count()}")
        
        # Show all faculty members
        all_faculty = FacultyMember.objects.all().order_by('name')
        self.stdout.write(f"Total Faculty Members: {all_faculty.count()}")
        
        # Show users without faculty records
        users_without_faculty = User.objects.filter(facultymember__isnull=True)
        self.stdout.write(f"\n--- USERS WITHOUT FACULTY RECORDS ({users_without_faculty.count()}) ---")
        for user in users_without_faculty:
            self.stdout.write(f"  ✗ {user.username} ({user.email}) - {user.first_name} {user.last_name}")
        
        # Show faculty members without user accounts
        faculty_without_users = FacultyMember.objects.filter(user__isnull=True)
        self.stdout.write(f"\n--- FACULTY WITHOUT USER ACCOUNTS ({faculty_without_users.count()}) ---")
        for faculty in faculty_without_users:
            self.stdout.write(f"  ✗ {faculty.name} ({faculty.email}) - {faculty.get_designation_display()}")
        
        # Show properly linked faculty
        linked_faculty = FacultyMember.objects.filter(user__isnull=False)
        self.stdout.write(f"\n--- PROPERLY LINKED FACULTY ({linked_faculty.count()}) ---")
        for faculty in linked_faculty:
            self.stdout.write(f"  ✓ {faculty.name} ↔ {faculty.user.username} ({faculty.user.email})")
        
        # Suggestions
        self.stdout.write(f"\n--- SUGGESTIONS ---")
        
        # Check for potential matches by email
        potential_matches = []
        for faculty in faculty_without_users:
            try:
                matching_user = User.objects.get(email=faculty.email)
                if not hasattr(matching_user, 'facultymember'):
                    potential_matches.append((faculty, matching_user))
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                continue
        
        if potential_matches:
            self.stdout.write(f"  📧 Found {len(potential_matches)} potential matches by email:")
            for faculty, user in potential_matches:
                self.stdout.write(f"     • {faculty.name} ↔ {user.username} (both have email: {faculty.email})")
                
        self.stdout.write(f"\n--- QUICK ACTIONS ---")
        self.stdout.write(f"  • To create a new faculty with user: python manage.py create_faculty --help")
        self.stdout.write(f"  • To auto-link by email: Use admin action 'Auto-link to users with matching emails'")
        self.stdout.write(f"  • To manually link: Go to Django admin → Faculty Members → Edit → Select User")
        
        self.stdout.write(self.style.SUCCESS('\n=== END OF REPORT ===\n'))