from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from .models import *
import os
from django.http import HttpResponse, Http404
from django.conf import settings
from .models import Notice_Board, FacultyMember, Chairman, Publication, Project, TechNews, ViewCount
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Event



def home(request):
    # Get important notices
    important_notices = Notice_Board.objects.filter(is_important=True)[:5]
    
    # Get latest notices (excluding important ones to avoid duplication)
    latest_notices = Notice_Board.objects.exclude(is_important=True)[:5]
    
    # Get latest notices
    latest_notices = Notice_Board.objects.all()[:5]
    
    # Get faculty members
    faculty_members = FacultyMember.objects.all()[:8]
    
    # Get current chairman
    current_chairman = Chairman.objects.filter(is_current=True).first()
    
    # Get latest tech news
    tech_news = TechNews.objects.all()[:3]
    
    # Get upcoming events first, then fill with latest events if needed
    upcoming_events = list(Event.objects.filter(
        is_upcoming=True,
        start_date__gte=timezone.now()
    ).order_by('start_date')[:3])

    # If we have less than 3 upcoming events, add latest events
    if len(upcoming_events) < 3:
        latest_events = Event.objects.exclude(
            id__in=[event.id for event in upcoming_events]
        ).order_by('-start_date')[:3 - len(upcoming_events)]
        upcoming_events.extend(latest_events)

    # Update view count for home page
    page_view, created = ViewCount.objects.get_or_create(page_name='home')
    page_view.increment()
    
    context = {
        'important_notices': important_notices,
        'latest_notices': latest_notices,
        'faculty_members': faculty_members,
        'current_chairman': current_chairman,
        'tech_news': tech_news,
        'events': upcoming_events,  # Pass events to the template

    }
    
    return render(request, 'cse/home.html', context)

#About nav bar
def why_neu_cse(request):
    return render(request, 'cse/about/why_neu_cse.html')
def message_from_department(request):
    return render(request, 'cse/about/message_from_department.html')
def message_from_chairman(request):
    return render(request, 'cse/about/message_from_chairman.html')
def facilities(request):
    return render(request, 'cse/about/facilities.html')
def history_neu_cse(request):
    return render(request, 'cse/about/history_neu_cse.html')
def mission_vision(request):
    return render(request, 'cse/about/mission_vision.html')
def history_neu(request):
    return render(request, 'cse/about/history_neu.html')
def achievements(request):
    return render(request, 'cse/about/achievements.html')


def notice_list(request):
    notice_type = request.GET.get('type')
    search_query = request.GET.get('search', '').strip()
    
    # Base queryset
    notices = Notice_Board.objects.all()
    
    # Apply type filter
    if notice_type == 'important':
        notices = notices.filter(is_important=True)
    elif notice_type == 'latest':
        notices = notices.order_by('-created_at')
    
    # Apply search filter if query exists
    if search_query:
        notices = notices.filter(title__icontains=search_query)
    
    # Update view count for notices page
    page_view, created = ViewCount.objects.get_or_create(page_name='notices')
    page_view.increment()
    
    return render(request, 'cse/notice_list.html', {
        'notices': notices, 
        'notice_type': notice_type,
        'search_query': search_query
    })

def notice_detail(request, pk):
    notice = get_object_or_404(Notice_Board, pk=pk)
    
    # Update view count for notice detail page
    page_view, created = ViewCount.objects.get_or_create(page_name=f'notice_{pk}')
    page_view.increment()
    
    # Check file type if a file exists
    file_type = None
    if notice.file:
        file_name = notice.file.name.lower()
        if file_name.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            file_type = 'image'
        elif file_name.endswith('.pdf'):
            file_type = 'pdf'
    
    return render(request, 'cse/notice_detail.html', {
        'notice': notice,
        'file_type': file_type
    })

def view_notice_file(request, pk):
    notice = get_object_or_404(Notice_Board, pk=pk)
    if notice.file:
        file_path = notice.file.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                file_name = notice.file.name.lower()
                if file_name.endswith('.pdf'):
                    content_type = 'application/pdf'
                elif file_name.endswith(('.png', '.jpg', '.jpeg')):
                    content_type = 'image/' + file_name.split('.')[-1]
                elif file_name.endswith('.gif'):
                    content_type = 'image/gif'
                else:
                    content_type = 'application/octet-stream'
                
                response = HttpResponse(fh.read(), content_type=content_type)
                return response
    raise Http404("File does not exist")

def download_notice(request, pk):
    notice = get_object_or_404(Notice_Board, pk=pk)
    if notice.file:
        file_path = notice.file.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                return response
    raise Http404("File does not exist")

def faculty_list(request):
    faculty_members = FacultyMember.objects.all()
    
    # Update view count for faculty page
    page_view, created = ViewCount.objects.get_or_create(page_name='faculty')
    page_view.increment()
    
    return render(request, 'cse/faculty_list.html', {'faculty_members': faculty_members})

def faculty_detail(request, pk):
    faculty = get_object_or_404(FacultyMember, pk=pk)
    return render(request, 'cse/faculty_detail.html', {'faculty': faculty})

def chairman_message(request):
    current_chairman = Chairman.objects.filter(is_current=True).first()
    
    # Update view count for chairman page
    page_view, created = ViewCount.objects.get_or_create(page_name='chairman')
    page_view.increment()
    
    return render(request, 'cse/chairman_message.html', {'chairman': current_chairman})

def publications(request):
    publications = Publication.objects.all()
    
    # Filter by type if provided
    pub_type = request.GET.get('type')
    if pub_type:
        publications = publications.filter(publication_type=pub_type)
    
    # Update view count for publications page
    page_view, created = ViewCount.objects.get_or_create(page_name='publications')
    page_view.increment()
    
    return render(request, 'cse/publications.html', {'publications': publications})

def projects(request):
    projects = Project.objects.all()
    
    # Filter by type if provided
    project_type = request.GET.get('type')
    if project_type:
        projects = projects.filter(project_type=project_type)
    
    # Update view count for projects page
    page_view, created = ViewCount.objects.get_or_create(page_name='projects')
    page_view.increment()
    
    return render(request, 'cse/projects.html', {'projects': projects})

def tech_news(request):
    news = TechNews.objects.all()
    
    # Update view count for tech news page
    page_view, created = ViewCount.objects.get_or_create(page_name='tech_news')
    page_view.increment()
    
    return render(request, 'cse/tech_news.html', {'news': news})

def about(request):
    # Update view count for about page
    page_view, created = ViewCount.objects.get_or_create(page_name='about')
    page_view.increment()
    
    return render(request, 'cse/about.html')

def events(request):
    # Get all upcoming events
    events_list = Event.objects.filter(is_upcoming=True).order_by('start_date')
    
    # Pagination - show 6 events per page
    paginator = Paginator(events_list, 6)
    page = request.GET.get('page')
    
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    
    context = {
        'events': events,
        'is_paginated': events.has_other_pages(),
    }
    return render(request, 'events/events.html', context)

def all_events(request):
    # Get search query
    query = request.GET.get('q')
    
    # Get all events, ordered by start date (upcoming first)
    events_list = Event.objects.all().order_by('start_date')
    
    # Apply search filter if query exists
    if query:
        events_list = events_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(organizer__icontains=query) |
            Q(event_type__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(events_list, 12)
    page = request.GET.get('page')
    
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    
    context = {
        'events': events,
        'query': query,
        'is_paginated': events.has_other_pages(),
    }
    return render(request, 'cse/all_events.html', context)

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    context = {
        'event': event
    }
    return render(request, 'cse/event_detail.html', context)