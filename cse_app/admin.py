from django.contrib import admin
from .models import *

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
    list_display = ('name', 'designation', 'email', 'is_chairman')
    list_filter = ('designation', 'is_chairman')
    search_fields = ('name', 'research_interest')

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