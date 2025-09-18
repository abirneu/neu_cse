from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import *
import os
from django.http import HttpResponse, Http404
from django.conf import settings
from .models import Notice_Board, FacultyMember, Chairman, Publication, Project, TechNews, ViewCount

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
    
    # Update view count for home page
    page_view, created = ViewCount.objects.get_or_create(page_name='home')
    page_view.increment()
    
    context = {
        'important_notices': important_notices,
        'latest_notices': latest_notices,
        'faculty_members': faculty_members,
        'current_chairman': current_chairman,
        'tech_news': tech_news,
    }
    
    return render(request, 'cse/home.html', context)

def notice_list(request):
    important_only = request.GET.get('important')
    
    if important_only:
        notices = Notice_Board.objects.filter(is_important=True)
    else:
        notices = Notice_Board.objects.all()
    
    # Update view count for notices page
    page_view, created = ViewCount.objects.get_or_create(page_name='notices')
    page_view.increment()
    
    return render(request, 'cse/notice_list.html', {'notices': notices, 'important_only': important_only})

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