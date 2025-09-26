from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cse_app.models import FacultyMember
from cse_app.admin import FacultyMemberAdminForm


class Command(BaseCommand):
    help = 'Debug the FacultyMemberAdminForm queryset'

    def handle(self, *args, **options):
        self.stdout.write("=== DEBUGGING FACULTY ADMIN FORM ===\n")
        
        # Test the form for a new faculty member
        self.stdout.write("--- Testing form for NEW faculty member ---")
        form = FacultyMemberAdminForm()
        available_users = form.fields['user'].queryset
        
        self.stdout.write(f"Available users count: {available_users.count()}")
        for user in available_users:
            self.stdout.write(f"  • {user.username} ({user.email}) - ID: {user.id}")
        
        # Test for existing faculty member (e.g., first one without user)
        faculty_without_user = FacultyMember.objects.filter(user__isnull=True).first()
        if faculty_without_user:
            self.stdout.write(f"\n--- Testing form for EXISTING faculty: {faculty_without_user.name} ---")
            form = FacultyMemberAdminForm(instance=faculty_without_user)
            available_users = form.fields['user'].queryset
            
            self.stdout.write(f"Available users count: {available_users.count()}")
            for user in available_users:
                self.stdout.write(f"  • {user.username} ({user.email}) - ID: {user.id}")
        
        # Show all users
        self.stdout.write(f"\n--- ALL USERS IN DATABASE ---")
        all_users = User.objects.all().order_by('username')
        self.stdout.write(f"Total users: {all_users.count()}")
        for user in all_users:
            linked_to = "✓ Linked" if hasattr(user, 'facultymember') else "✗ Available"
            self.stdout.write(f"  • {user.username} ({user.email}) - ID: {user.id} - {linked_to}")
        
        # Show used user IDs
        used_users = FacultyMember.objects.values_list('user_id', flat=True).filter(user_id__isnull=False)
        self.stdout.write(f"\n--- USED USER IDs ---")
        self.stdout.write(f"Used user IDs: {list(used_users)}")
        
        self.stdout.write("\n=== END DEBUG ===")