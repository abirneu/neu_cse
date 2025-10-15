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
# DEPARTMENT STATISTICS ADMIN
# =====================================

class DepartmentStatisticsForm(forms.ModelForm):
    class Meta:
        model = DepartmentStatistics
        fields = '__all__'
        help_texts = {
            'total_students': '✏️ Enter the total number of students (manual entry required)',
            'total_faculty': '🔄 Enter number OR set to 0 for auto-count from database',
            'total_labs': '✏️ Enter the number of computer labs (manual entry required)',
            'total_research_areas': '🔄 Enter number OR set to 0 for auto-count from database',
            'total_publications': '🔄 Enter number OR set to 0 for auto-count from database',
            'total_projects': '🔄 Enter number OR set to 0 for auto-count from database',
        }

@admin.register(DepartmentStatistics)
class DepartmentStatisticsAdmin(admin.ModelAdmin):
    form = DepartmentStatisticsForm
    
    fieldsets = (
        (' Basic Statistics', {
            'fields': ('total_students', 'total_faculty', 'total_labs', 'total_research_areas'),
            'description': '<div style="background: #e3f2fd; padding: 15px; border-left: 4px solid #2196f3; margin-bottom: 15px;"><strong>💡 How to use:</strong><br>• <strong>Manual entry:</strong> Students, Labs - Enter your desired number<br>• <strong>Auto-calculate:</strong> Faculty, Research Areas - Set to <strong>0</strong> to automatically count from database<br>• Current database counts will be shown below each field</div>'
        }),
        (' Research & Academic Statistics', {
            'fields': ('total_publications', 'total_projects'),
            'description': '<div style="background: #f3e5f5; padding: 15px; border-left: 4px solid #9c27b0; margin-bottom: 15px;"><strong>💡 Auto-calculation available:</strong><br>Set to <strong>0</strong> to automatically count from Publications and Projects in database</div>'
        }),
    )
    
    readonly_fields = ()
    
    list_display = (
        'get_edit_link',
        'total_students',
        'get_faculty_display',
        'total_labs',
        'get_research_areas_display',
        'get_publications_display',
        'get_projects_display',
        'last_updated'
    )
    
    # Make all fields clickable for editing
    list_display_links = (
        'get_edit_link',
        'total_students',
        'get_faculty_display',
        'total_labs',
        'get_research_areas_display',
        'get_publications_display',
        'get_projects_display',
    )
    
    def get_edit_link(self, obj):
        return format_html(
            '<strong style="color: #417690;">✏️ EDIT</strong>'
        )
    get_edit_link.short_description = 'Click Any Field to Edit →'
    
    def get_faculty_display(self, obj):
        actual = obj.get_faculty_count()
        if obj.total_faculty == 0:
            return format_html('<span style="color: green;">✓ {} (Auto)</span>', actual)
        return format_html('{} <span style="color: gray;">(Actual: {})</span>', obj.total_faculty, actual)
    get_faculty_display.short_description = 'Faculty'
    
    def get_research_areas_display(self, obj):
        actual = obj.get_research_areas_count()
        if obj.total_research_areas == 0:
            return format_html('<span style="color: green;">✓ {} (Auto)</span>', actual)
        return format_html('{} <span style="color: gray;">(Actual: {})</span>', obj.total_research_areas, actual)
    get_research_areas_display.short_description = 'Research Areas'
    
    def get_publications_display(self, obj):
        actual = obj.get_publications_count()
        if obj.total_publications == 0:
            return format_html('<span style="color: green;">✓ {} (Auto)</span>', actual)
        return format_html('{} <span style="color: gray;">(Actual: {})</span>', obj.total_publications, actual)
    get_publications_display.short_description = 'Publications'
    
    def get_projects_display(self, obj):
        actual = obj.get_projects_count()
        if obj.total_projects == 0:
            return format_html('<span style="color: green;">✓ {} (Auto)</span>', actual)
        return format_html('{} <span style="color: gray;">(Actual: {})</span>', obj.total_projects, actual)
    get_projects_display.short_description = 'Projects'
    
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not DepartmentStatistics.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False
    
    def changelist_view(self, request, extra_context=None):
        """Add custom message and instructions to changelist"""
        extra_context = extra_context or {}
        extra_context['title'] = 'Department Statistics'
        
        # Add a custom message
        from django.contrib import messages
        if DepartmentStatistics.objects.exists():
            messages.info(
                request, 
                ' Click on any field in the row below to EDIT the department statistics. '
                'You can update student count, labs, and other values.'
            )
        else:
            messages.warning(
                request,
                ' No statistics record found. Click "Add Department Statistics" to create one.'
            )
        
        return super().changelist_view(request, extra_context=extra_context)
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Add helper message to change view"""
        extra_context = extra_context or {}
        from django.contrib import messages
        
        obj = self.get_object(request, object_id)
        if obj:
            messages.success(
                request,
                f' Editing Department Statistics. Current values shown below. '
                f'Set numeric fields to 0 for auto-calculation.'
            )
        
        return super().change_view(request, object_id, form_url, extra_context)
    
    class Media:
        css = {
            'all': ('admin/css/custom_stats_admin.css',)
        }
        js = ('admin/js/custom_stats_admin.js',)


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