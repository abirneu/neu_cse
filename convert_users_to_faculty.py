# Quick script to convert existing Users to Faculty Members
# Run: python manage.py shell
# Then copy and paste this script:

from django.contrib.auth.models import User
from cse_app.models import FacultyMember

# Get all users that don't have faculty member records
users_without_faculty = User.objects.exclude(
    id__in=FacultyMember.objects.values_list('user_id', flat=True)
)

print(f"Found {users_without_faculty.count()} users without faculty records:")

for user in users_without_faculty:
    print(f"- {user.username} ({user.email})")
    
    # Ask for confirmation before creating
    create = input(f"Create faculty record for {user.username}? (y/n): ")
    
    if create.lower() == 'y':
        # Choose designation
        print("Available designations:")
        print("1. assistant_professor")
        print("2. associate_professor") 
        print("3. professor")
        print("4. lecturer")
        print("5. chairman")
        
        designation_choice = input("Enter number (1-5): ")
        designation_map = {
            '1': 'assistant_professor',
            '2': 'associate_professor',
            '3': 'professor',
            '4': 'lecturer',
            '5': 'chairman'
        }
        
        designation = designation_map.get(designation_choice, 'assistant_professor')
        
        # Create faculty member
        faculty = FacultyMember.objects.create(
            user=user,
            name=f"{user.first_name} {user.last_name}".strip() or user.username,
            designation=designation,
            status='active',
            member_type='full_time',
            email=user.email,
        )
        
        print(f"✅ Created faculty record for {faculty.name}")
    else:
        print("⏭️  Skipped")

print("\n✅ Done! All users should now be able to login as faculty.")