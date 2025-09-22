from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from .models import *
import os
from django.http import HttpResponse, Http404
from django.conf import settings
from .models import Notice_Board, FacultyMember, Chairman, Publication, Project, TechNews, ViewCount, ImageGallery, StaffProfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Event
from .models import ScrollingNotice
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import NoticeForm, ScrollingNoticeForm

def staff_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                staff_profile = StaffProfile.objects.get(user=user)
                if staff_profile.is_active:
                    login(request, user)
                    return redirect('staff_dashboard')
                else:
                    messages.error(request, 'Your account is not active. Please contact the administrator.')
            except StaffProfile.DoesNotExist:
                messages.error(request, 'You are not registered as staff.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'cse/staff/login.html')

@login_required
def staff_logout(request):
    # Clear any pending messages before logout
    if 'dashboard_message' in request.session:
        del request.session['dashboard_message']
    request.session.flush()
    logout(request)
    return redirect('staff_login')

@login_required(login_url='staff_login')
def create_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.created_by = request.user
            notice.save()
            request.session['temp_message'] = {
                'type': 'success',
                'message': 'Notice created successfully!'
            }
            request.session.modified = True
            return redirect('staff_dashboard')
        else:
            request.session['temp_message'] = {
                'type': 'error',
                'message': 'Error creating notice. Please check the form.'
            }
            request.session.modified = True
    return redirect('staff_dashboard')

@login_required
@login_required
def create_scrolling_notice(request):
    if request.method == 'POST':
        form = ScrollingNoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.created_by = request.user
            notice.save()
            request.session['temp_message'] = {
                'type': 'success',
                'message': 'Scrolling notice created successfully!'
            }
            request.session.modified = True
            return redirect('staff_dashboard')
        else:
            request.session['temp_message'] = {
                'type': 'error',
                'message': 'Error creating scrolling notice. Please check the form.'
            }
            request.session.modified = True
    return redirect('staff_dashboard')

@login_required
@login_required(login_url='staff_login')
def staff_dashboard(request):
    try:
        staff_profile = StaffProfile.objects.get(user=request.user)
        if not staff_profile.is_active:
            messages.error(request, 'Your account is not active. Please contact the administrator.')
            logout(request)
            return redirect('staff_login')
            
        notice_form = NoticeForm()
        scrolling_notice_form = ScrollingNoticeForm()
        
        # Get user's notices and statistics
        user_notices = Notice_Board.objects.filter(created_by=request.user).order_by('-created_at')
        user_scrolling_notices = ScrollingNotice.objects.filter(created_by=request.user).order_by('-created_at')
        
        # Get all statistics
        total_notices = Notice_Board.objects.count()
        total_scrolling_notices = ScrollingNotice.objects.count()
        staff_notices = user_notices.count()
        staff_scrolling_notices = user_scrolling_notices.count()
        
        # Get temporary message and remove it from session
        temp_message = None
        if 'temp_message' in request.session:
            temp_message = request.session.pop('temp_message')
            request.session.modified = True

        context = {
            'staff_profile': staff_profile,
            'total_notices': total_notices,
            'total_scrolling_notices': total_scrolling_notices,
            'staff_notices': staff_notices,
            'staff_scrolling_notices': staff_scrolling_notices,
            'notice_form': notice_form,
            'scrolling_notice_form': scrolling_notice_form,
            'user_notices': user_notices,
            'user_scrolling_notices': user_scrolling_notices,
            'recent_notices': Notice_Board.objects.order_by('-created_at')[:5],
            'temp_message': temp_message,  # Add temporary message to context
        }
        return render(request, 'cse/staff/dashboard.html', context)
    except StaffProfile.DoesNotExist:
        logout(request)
        messages.error(request, 'You are not registered as staff.')
        return redirect('staff_login')



@login_required(login_url='staff_login')
def edit_notice(request, pk):
    notice = get_object_or_404(Notice_Board, pk=pk)
    
    # Check if the user is the creator of the notice
    if notice.created_by != request.user:
        request.session['temp_message'] = {
            'type': 'error',
            'message': "You don't have permission to edit this notice."
        }
        request.session.modified = True
        return redirect('staff_dashboard')
    
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.created_by = request.user  # Ensure created_by is set
            notice.save()
            request.session['temp_message'] = {
                'type': 'success',
                'message': 'Notice updated successfully!'
            }
            request.session.modified = True
            return redirect('staff_dashboard')
        else:
            request.session['temp_message'] = {
                'type': 'error',
                'message': 'Error updating notice. Please check the form.'
            }
            request.session.modified = True
    else:
        form = NoticeForm(instance=notice)
    
    return render(request, 'cse/staff/edit_notice.html', {
        'form': form,
        'notice': notice
    })

@login_required(login_url='staff_login')
def delete_notice(request, pk):
    notice = get_object_or_404(Notice_Board, pk=pk)
    
    # Check if the user is the creator of the notice
    if notice.created_by != request.user:
        request.session['temp_message'] = {
            'type': 'error',
            'message': "You don't have permission to delete this notice."
        }
        request.session.modified = True
        return redirect('staff_dashboard')
    
    if request.method == 'POST':
        # Delete the associated file if it exists
        if notice.file:
            if os.path.isfile(notice.file.path):
                try:
                    os.remove(notice.file.path)
                except (OSError, FileNotFoundError):
                    pass  # Ignore file deletion errors
        
        notice.delete()
        request.session['temp_message'] = {
            'type': 'success',
            'message': 'Notice deleted successfully!'
        }
        request.session.modified = True
        return redirect('staff_dashboard')
    
    return render(request, 'cse/staff/delete_notice_confirm.html', {
        'notice': notice
    })

@login_required(login_url='staff_login')
def edit_scrolling_notice(request, pk):
    notice = get_object_or_404(ScrollingNotice, pk=pk)
    
    # Check if the user is the creator of the notice
    if notice.created_by != request.user:
        request.session['temp_message'] = {
            'type': 'error',
            'message': "You don't have permission to edit this scrolling notice."
        }
        request.session.modified = True
        return redirect('staff_dashboard')
    
    if request.method == 'POST':
        form = ScrollingNoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            request.session['temp_message'] = {
                'type': 'success',
                'message': 'Scrolling notice updated successfully!'
            }
            request.session.modified = True
            return redirect('staff_dashboard')
    else:
        form = ScrollingNoticeForm(instance=notice)
    
    return render(request, 'cse/staff/edit_scrolling_notice.html', {
        'form': form,
        'notice': notice
    })

@login_required(login_url='staff_login')
def delete_scrolling_notice(request, pk):
    notice = get_object_or_404(ScrollingNotice, pk=pk)
    
    # Check if the user is the creator of the notice
    if notice.created_by != request.user:
        request.session['temp_message'] = {
            'type': 'error',
            'message': "You don't have permission to delete this scrolling notice."
        }
        request.session.modified = True
        return redirect('staff_dashboard')
    
    if request.method == 'POST':
        notice.delete()
        request.session['temp_message'] = {
            'type': 'success',
            'message': 'Scrolling notice deleted successfully!'
        }
        request.session.modified = True
        return redirect('staff_dashboard')
    
    return render(request, 'cse/staff/delete_scrolling_notice_confirm.html', {
        'notice': notice
    })

def home(request):
    # Get active carousel items ordered by their specified order
    carousel_items = CarouselItem.objects.filter(is_active=True).order_by('order')
    
    # Get the latest 6 images for the gallery section
    latest_images = ImageGallery.objects.all().order_by('-upload_time')[:6]

    # Get important notices
    important_notices = Notice_Board.objects.filter(is_important=True)[:5]
    
    # Get latest notices (excluding important ones to avoid duplication)
    latest_notices = Notice_Board.objects.exclude(is_important=True)[:5]
    
    # Get the latest 3 projects
    latest_projects = Project.objects.all().order_by('-start_date')[:3]

    # Get the latest 3 publications
    latest_publications = Publication.objects.all().order_by('-publication_date')[:3]

    # Get the latest events
    latest_events = Event.objects.all().order_by('-start_date')[:3]
    
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
    
    context = {
        'carousel_items': carousel_items,
        'important_notices': important_notices,
        'latest_notices': latest_notices,
        'faculty_members': faculty_members,
        'current_chairman': current_chairman,
        'tech_news': tech_news,
        'events': upcoming_events,  # Pass events to the template
        'latest_projects': latest_projects,
        'latest_publications': latest_publications,
        'images': latest_images,
        
    }
    
    page_view, created = ViewCount.objects.get_or_create(page_name='home')
    page_view.increment()
    
    # Add latest images to context
    # context['images'] = latest_images
    
    return render(request, 'cse/home.html', context)


#About nav bar
def why_neu_cse(request):
    return render(request, 'cse/about/why_neu_cse.html')
def message_from_department(request):
    return render(request, 'cse/about/message_from_department.html')
def message_from_chairman(request):
    # Get current chairman
    current_chairman = Chairman.objects.filter(is_current=True).first()
    
    # Update view count for chairman's message page
    page_view, created = ViewCount.objects.get_or_create(page_name='chairman_message')
    page_view.increment()
    
    return render(request, 'cse/about/message_from_chairman.html', {
        'current_chairman': current_chairman
    })
def facilities(request):
    return render(request, 'cse/about/facilities.html')
def history_neu_cse(request):
    return render(request, 'cse/about/history_neu_cse.html')
def mission_vision(request):
    return render(request, 'cse/about/mission_vission.html')
def history_neu(request):
    return render(request, 'cse/about/history_neu.html')
def achievements(request):
    return render(request, 'cse/about/achievements.html')

#faculty and staff nav bar
def active_faculty(request):
    active_faculty_members = FacultyMember.objects.filter(status='active')
    return render(request, 'cse/faculty_and_staff/active_faculty.html', {
        'faculty_members': active_faculty_members
    })
def ex_chairman(request):
    # Get all ex-chairmen ordered by most recent first
    ex_chairmen = Chairman.objects.filter(is_current=False).order_by('-to_date')
    
    # For each chairman, ensure we have their faculty details
    for chairman in ex_chairmen:
        if chairman.faculty:
            chairman.name = chairman.faculty.name
            chairman.image = chairman.faculty.image
            chairman.email = chairman.faculty.email
            chairman.designation = chairman.faculty.get_designation_display()
            chairman.tenure_start = chairman.from_date
            chairman.tenure_end = chairman.to_date

    return render(request, 'cse/faculty_and_staff/ex_chariman.html', {
        'ex_chairmen': ex_chairmen
    })
def faculty_on_leave(request):
    faculty_on_leave = FacultyMember.objects.filter(status='on_leave')
    return render(request, 'cse/faculty_and_staff/faculty_on_leave.html', {
        'faculty_members': faculty_on_leave
    })
def past_faculty(request):
    past_faculty_members = FacultyMember.objects.filter(status='past_faculty').order_by('-end_date')
    return render(request, 'cse/faculty_and_staff/past_faculty.html', {
        'faculty_members': past_faculty_members
    })
    
def officer_and_staff(request):
    staff_members = Staff.objects.all()
    return render(request, 'cse/faculty_and_staff/officer_and_staff.html', {
        'staff_members': staff_members
    })

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
    
    # Pagination - 7 notices per page
    paginator = Paginator(notices, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'notices': page_obj,  # This allows backward compatibility with existing template
        'notice_type': notice_type,
        'search_query': search_query,
    }
    
    return render(request, 'cse/notice_list.html', context)

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
    # Get filter parameter from request
    status = request.GET.get('status', 'active')  # Default to active
    
    # Start with all faculty members
    faculty_members = FacultyMember.objects.all()
    
    # Apply status filter
    if status != 'all':
        faculty_members = faculty_members.filter(status=status)
    
    # Get distinct statuses for filter options
    statuses = FacultyMember.objects.values_list('status', flat=True).distinct()
    
    # Update view count for faculty page
    page_view, created = ViewCount.objects.get_or_create(page_name='faculty')
    page_view.increment()
    
    context = {
        'faculty_members': faculty_members,
        'statuses': statuses,
        'current_status': status,
    }
    
    return render(request, 'cse/faculty_list.html', context)

def staff_list(request):
    # Get filter parameters from request
    staff_type = request.GET.get('type', 'all')  # Default to all
    status = request.GET.get('status', 'active')  # Default to active
    
    # Start with all staff members
    staff_members = Staff.objects.all()
    
    # Apply filters
    if staff_type != 'all':
        staff_members = staff_members.filter(staff_type=staff_type)
    
    if status != 'all':
        staff_members = staff_members.filter(status=status)
    
    # Get distinct statuses for filter options
    statuses = Staff.objects.values_list('status', flat=True).distinct()
    
    # Update view count for staff page
    page_view, created = ViewCount.objects.get_or_create(page_name='staff')
    page_view.increment()
    
    context = {
        'staff_members': staff_members,
        'staff_types': dict(Staff.STAFF_TYPE_CHOICES),
        'statuses': statuses,
        'current_type': staff_type,
        'current_status': status,
    }
    
    return render(request, 'cse/staff_list.html', context)

def faculty_detail(request, pk):
    faculty = get_object_or_404(FacultyMember, pk=pk)
    return render(request, 'cse/faculty_detail.html', {'faculty': faculty})

def chairman_message(request):
    # Get current chairman
    current_chairman = Chairman.objects.filter(is_current=True).first()
    
    # Update view count for chairman page
    page_view, created = ViewCount.objects.get_or_create(page_name='chairman')
    page_view.increment()
    
    context = {
        'current_chairman': current_chairman,
        'page_view': page_view,
    }
    return render(request, 'message_from_chairman.html', context)

def publications_home(request):
    latest_publications = Publication.objects.all().order_by('-publication_date')[:3]
    return render(request, 'cse/publications.html', {'latest_publications': latest_publications})

def all_publications(request):
    publications = Publication.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        publications = publications.filter(title__icontains=search_query)
    
    # Sort publications
    sort_by = request.GET.get('sort', 'date')  # Default sort by date
    if sort_by == 'date':
        publications = publications.order_by('-publication_date')
    elif sort_by == 'title':
        publications = publications.order_by('title')
    
    # Pagination
    paginator = Paginator(publications, 8)  # Show 8 publications per page
    page = request.GET.get('page')
    try:
        publications = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        publications = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        publications = paginator.page(paginator.num_pages)
        
    return render(request, 'cse/all_publications.html', {'publications': publications})

def publication_detail(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    return render(request, 'cse/publication_detail.html', {'publication': publication})
    if sort_by == 'date':
        publications = publications.order_by('-publication_date')
    elif sort_by == 'title':
        publications = publications.order_by('title')
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
    
    return render(request, 'cse/projects/projects.html', {'projects': projects})

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

def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    context = {
        'project': project
    }
    return render(request, 'cse/projects/project_detail.html', context)

def all_projects(request):
    projects_list = Project.objects.all().order_by('-start_date')
    
    # Pagination
    paginator = Paginator(projects_list, 9)  # Show 9 projects per page
    page = request.GET.get('page')
    
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)
    
    context = {
        'projects': projects,
        'is_paginated': projects.has_other_pages(),
    }
    return render(request, 'cse/projects/all_projects.html', context)

def projects(request):
    # Redirect to all_projects view
    return redirect('all_projects')

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    context = {
        'event': event
    }
    return render(request, 'cse/event_detail.html', context)

def alumni(request):
    return render(request, 'cse/alumni.html')

def computer_club(request):
    # Get all club members and sort them by priority level and position
    club_members = ComputerClubMember.objects.all()
    
    # Group members by priority level
    core_leadership = [m for m in club_members if m.get_priority_level() == 1]
    key_operations = [m for m in club_members if m.get_priority_level() == 2]
    support_roles = [m for m in club_members if m.get_priority_level() == 3]
    
    context = {
        'core_leadership': core_leadership,
        'key_operations': key_operations,
        'support_roles': support_roles,
    }
    
    return render(request, 'cse/club/computer_club.html', context)

def programming_club(request):
    return render(request, 'cse/club/programming_club.html')

def contact_us(request):
    return render(request, 'cse/contact_us.html')

def image_gallery_home(request):
    # Get the latest 6 images for the home page
    images = ImageGallery.objects.all().order_by('-upload_time')[:6]
    return render(request, 'cse/image_gallery/home_page_image.html', {'images': images})

def all_images(request):
    image_list = ImageGallery.objects.all().order_by('-upload_time')
    paginator = Paginator(image_list, 9)  # Show 9 images per page
    
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    
    return render(request, 'cse/image_gallery/all_image.html', {'images': images})