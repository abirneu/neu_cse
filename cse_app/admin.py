from django.contrib import admin
from django.utils.html import format_html
from .models import *

# =====================================
# FACULTY MANAGEMENT SECTION
# =====================================

# Inline classes for Faculty-related models
class EducationInline(admin.TabularInline):
    model = Education
    extra = 1
    fields = ('degree_name', 'major_subject', 'board_institute', 'country', 'passing_year', 'grade_gpa', 'order')

class ProfessionalExperienceInline(admin.TabularInline):
    model = ProfessionalExperience
    extra = 1
    fields = ('organization', 'position_title', 'location', 'start_date', 'end_date', 'is_current', 'description', 'order')

class PublicationRecordInline(admin.TabularInline):
    model = PublicationRecord
    extra = 1
    fields = ('title', 'authors', 'publication_type', 'venue', 'year', 'order')

class AwardRecordInline(admin.TabularInline):
    model = AwardRecord
    extra = 1
    fields = ('award_title', 'award_type', 'awarding_organization', 'year', 'order')

class CourseRecordInline(admin.TabularInline):
    model = CourseRecord
    extra = 1
    fields = ('course_code', 'course_title', 'course_level', 'course_type', 'semester', 'credit_hours', 'order')

class MembershipRecordInline(admin.TabularInline):
    model = MembershipRecord
    extra = 1
    fields = ('organization_name', 'membership_type', 'position', 'start_date', 'end_date', 'is_current', 'order')

@admin.register(FacultyMember)
class FacultyMemberAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'designation', 
        'status', 
        'email', 
        'phone', 
        'joined_date',
        'is_chairman'
    )
    list_filter = ('designation', 'status', 'member_type', 'is_chairman', 'joined_date')
    search_fields = ('name', 'email', 'phone', 'research_interest', 'bio')
    
    # Enhanced inlines for comprehensive faculty profile management
    inlines = [
        EducationInline,
        ProfessionalExperienceInline, 
        PublicationRecordInline,
        AwardRecordInline,
        CourseRecordInline,
        MembershipRecordInline,
    ]
    
    date_hierarchy = 'joined_date'
    ordering = ('designation', 'name')
    
    # Organized fieldsets for better UX
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('name', 'designation'),
                ('status', 'member_type'),
                ('is_chairman', 'image')
            ),
        }),
        
        ('Account Management', {
            'fields': ('user',),
            'classes': ('collapse',),
            'description': 'Link this faculty member to a user account for login access (optional).'
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
                'others'
            ),
            'classes': ('collapse',),
            'description': 'Upload CV/Resume and add any other relevant information not covered by the structured sections below.'
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