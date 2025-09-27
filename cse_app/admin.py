from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.contrib.auth.models import User
from .models import *


# Custom form for FacultyMember to show only available users
class FacultyMemberAdminForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.none(),  # Will be set in __init__
        empty_label="--- Select User Account ---",
        required=False,
        help_text="Select a user account to link with this faculty member. Only shows users not already linked.",
        widget=forms.Select(attrs={'style': 'min-width: 200px;'})
    )
    
    class Meta:
        model = FacultyMember
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get users that are already linked to faculty (exclude current instance)
        used_user_ids = FacultyMember.objects.exclude(
            pk=self.instance.pk if self.instance and self.instance.pk else None
        ).filter(user__isnull=False).values_list('user_id', flat=True)
        
        # Get available users (not already linked)
        available_users = User.objects.exclude(id__in=used_user_ids).order_by('username')
        
        # Set the queryset for user field
        self.fields['user'].queryset = available_users
        
        # Add some debugging info to help text
        count = available_users.count()
        self.fields['user'].help_text = (
            f"Select a user account to link ({count} available users). "
            "Only shows users not already linked to other faculty members."
        )

# =====================================
# FACULTY MANAGEMENT SECTION
# =====================================

# Inline classes for Faculty-related models (only for table-based fields)
class EducationInline(admin.TabularInline):
    model = Education
    extra = 1
    fields = ('degree_name', 'major_subject', 'board_institute', 'country', 'passing_year', 'grade_gpa', 'order')

class ProfessionalExperienceInline(admin.TabularInline):
    model = ProfessionalExperience
    extra = 1
    fields = ('organization', 'position_title', 'location', 'start_date', 'end_date', 'is_current', 'description', 'order')

# The following inlines are removed as per requirements - using rich text fields instead:
# - PublicationRecordInline (use 'publications' rich text field)
# - AwardRecordInline (use 'awards_honors' rich text field)  
# - CourseRecordInline (use 'courses_taught' rich text field)
# - MembershipRecordInline (use 'membership' rich text field)

@admin.register(FacultyMember)
class FacultyMemberAdmin(admin.ModelAdmin):
    form = FacultyMemberAdminForm  # Use custom form
    
    list_display = (
        'name', 
        'designation', 
        'status', 
        'email', 
        'phone', 
        'linked_user',
        'joined_date',
        'is_current',
        'is_chairman'
    )
    list_filter = ('designation', 'status', 'member_type', 'is_current', 'is_chairman', 'joined_date')
    search_fields = ('name', 'email', 'phone', 'research_interest', 'bio', 'user__username')
    
    # Enhanced inlines for comprehensive faculty profile management
    # Only structured table data (Education and Professional Experience)
    inlines = [
        EducationInline,
        ProfessionalExperienceInline, 
    ]
    
    date_hierarchy = 'joined_date'
    ordering = ('designation', 'name')
    
    def linked_user(self, obj):
        """Display linked user in list view"""
        if obj.user:
            return format_html('<span style="color: green;">✓ {}</span>', obj.user.username)
        return format_html('<span style="color: red;">✗ No User</span>')
    linked_user.short_description = 'Linked User'
    linked_user.admin_order_field = 'user'
    
    def get_form(self, request, obj=None, **kwargs):
        """Customize form display"""
        form = super().get_form(request, obj, **kwargs)
        return form
    
    actions = ['link_users_automatically', 'show_available_users_debug']
    
    def link_users_automatically(self, request, queryset):
        """Auto-link faculty members to users with matching emails"""
        linked_count = 0
        for faculty in queryset.filter(user__isnull=True):
            try:
                # Try to find user with matching email
                user = User.objects.get(email=faculty.email)
                # Check if user is not already linked
                if not hasattr(user, 'facultymember'):
                    faculty.user = user
                    faculty.save()
                    linked_count += 1
            except User.DoesNotExist:
                continue
            except User.MultipleObjectsReturned:
                continue
        
        self.message_user(request, f'Successfully linked {linked_count} faculty members to user accounts.')
    link_users_automatically.short_description = "Auto-link to users with matching emails"
    
    def show_available_users_debug(self, request, queryset):
        """Debug action to show available users"""
        form = FacultyMemberAdminForm()
        available_users = form.fields['user'].queryset
        user_list = ', '.join([u.username for u in available_users])
        self.message_user(request, f'Available users ({available_users.count()}): {user_list}')
    show_available_users_debug.short_description = "Debug: Show available users"
    
    # Organized fieldsets for better UX
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('name', 'designation'),
                ('status', 'member_type'),
                ('is_chairman', 'image')
            ),
        }),
        
        ('User Account Linking', {
            'fields': ('user',),
            'description': 'Select a user account to link with this faculty member. This allows them to login to the faculty dashboard. Leave blank if no login access is needed.',
            'classes': ('wide',),
        }),
        
        ('Contact Information', {
            'fields': (
                ('email', 'phone'),
                'room_no'
            ),
        }),
        
        ('Professional Profile', {
            'fields': (
                'bio',
                'research_interest'
            ),
        }),
        
        ('Academic & Social Links', {
            'fields': (
                ('research_gate_url', 'google_scholar_url'),
                ('orcid_url', 'linkedin_url'),
                'personal_website'
            ),
            'classes': ('collapse',)
        }),
        
        ('Documents & Additional Info', {
            'fields': (
                'cv_file',
            ),
            'classes': ('collapse',),
            'description': 'Upload CV/Resume.'
        }),
        
        ('Rich Text Fields', {
            'fields': (
                'research_activities',
                'publications',
                'courses_taught', 
                'membership',
                'awards_honors',
                'others'
            ),
            'classes': ('collapse',),
            'description': 'Rich text fields for detailed information. Use the structured tables above for Education and Professional Experience.'
        }),
        
        ('Administrative Information', {
            'fields': (
                ('joined_date', 'end_date'),
            ),
            'classes': ('collapse',)
        }),
    )


# =====================================
# OTHER MODELS - BASIC ADMIN
# =====================================

admin.site.register(Notice_Board)
admin.site.register(ScrollingNotice)
admin.site.register(Event)
admin.site.register(Project)
admin.site.register(Staff)
admin.site.register(StaffProfile)
admin.site.register(Chairman)
admin.site.register(ComputerClubMember)
admin.site.register(CarouselItem)
admin.site.register(ImageGallery)
admin.site.register(TechNews)