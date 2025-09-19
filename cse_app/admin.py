from django.contrib import admin
from .models import *
from .models import ScrollingNotice

@admin.register(ScrollingNotice)
class ScrollingNoticeAdmin(admin.ModelAdmin):
    list_display = ('text', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('text',)

@admin.register(Notice_Board)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_important')
    list_filter = ('created_at', 'is_important')
    search_fields = ('title', 'content')

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'publication_type', 'publication_date')
    list_filter = ('publication_type', 'publication_date')
    search_fields = ('title', 'authors')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_type', 'start_date', 'is_ongoing')
    list_filter = ('project_type', 'start_date', 'is_ongoing')
    filter_horizontal = ('members',)
    search_fields = ('title', 'description')

@admin.register(FacultyMember)
class FacultyMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'status', 'email', 'is_chairman')
    list_filter = ('designation', 'status', 'is_chairman')
    search_fields = ('name', 'email', 'research_interest', 'bio')
    fieldsets = (
        (None, {
            'fields': ('name', 'designation', 'status', 'is_chairman')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'room_no')
        }),
        ('Profile', {
            'fields': ('bio', 'education', 'research_interest', 'image')
        }),
        ('Dates', {
            'fields': ('joined_date', 'end_date')
        }),
    )

@admin.register(Chairman)
class ChairmanAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'from_date', 'to_date', 'is_current')
    list_filter = ('is_current', 'from_date')

@admin.register(TechNews)
class TechNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'published_date')
    list_filter = ('published_date', 'source')
    search_fields = ('title', 'content')

@admin.register(ViewCount)
class ViewCountAdmin(admin.ModelAdmin):
    list_display = ('page_name', 'count', 'last_updated')
    readonly_fields = ('page_name', 'count', 'last_updated')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'start_date', 'end_date', 'location', 'is_upcoming')
    list_filter = ('event_type', 'is_upcoming', 'start_date')
    search_fields = ('title', 'description', 'location', 'organizer')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'event_type')
        }),
        ('Date & Time', {
            'fields': ('start_date', 'end_date')
        }),
        ('Location & Organizer', {
            'fields': ('location', 'organizer')
        }),
        ('Media & Links', {
            'fields': ('image', 'registration_link')
        }),
    )

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'staff_type', 'designation', 'status', 'email')
    list_filter = ('staff_type', 'status', 'designation')
    search_fields = ('name', 'email', 'bio', 'responsibilities')
    fieldsets = (
        (None, {
            'fields': ('name', 'staff_type', 'designation', 'status')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'room_no')
        }),
        ('Details', {
            'fields': ('bio', 'responsibilities', 'image')
        }),
        ('Dates', {
            'fields': ('joined_date', 'end_date')
        }),
    )
