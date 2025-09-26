# Django shell commands to create faculty member
# Run: python manage.py shell
# Then copy and paste these commands:

from django.contrib.auth.models import User
from cse_app.models import FacultyMember

# Step 1: Create a User
user = User.objects.create_user(
    username='faculty_username',  # Change this
    password='your_password',     # Change this
    first_name='John',           # Change this
    last_name='Doe',             # Change this
    email='john.doe@example.com' # Change this
)

# Step 2: Create FacultyMember linked to this user
faculty = FacultyMember.objects.create(
    user=user,
    name=f"{user.first_name} {user.last_name}",
    designation='assistant_professor',  # Choose from: professor, associate_professor, assistant_professor, lecturer, chairman
    status='active',                    # Choose from: active, on_leave, ex_chairman, past_faculty
    member_type='full_time',           # Choose from: full_time, part_time, visiting, adjunct
    email=user.email,
    # Add other optional fields as needed:
    # phone='123-456-7890',
    # room_no='Room 101',
    # bio='Faculty biography here...',
    # research_interest='Research interests here...',
)

print(f"Faculty member created successfully: {faculty.name}")