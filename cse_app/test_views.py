from django.http import JsonResponse
from django.contrib.auth.models import User
from cse_app.models import FacultyMember
from cse_app.admin import FacultyMemberAdminForm


def test_faculty_form(request):
    """Test endpoint to check available users in faculty form"""
    form = FacultyMemberAdminForm()
    available_users = form.fields['user'].queryset
    
    users_data = []
    for user in available_users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })
    
    return JsonResponse({
        'available_users_count': available_users.count(),
        'available_users': users_data,
        'help_text': form.fields['user'].help_text
    })