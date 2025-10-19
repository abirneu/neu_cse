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
from .forms import NoticeForm, ScrollingNoticeForm, FacultyMemberForm, EducationForm, ProfessionalExperienceForm, StaffProfileForm

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

@login_required(login_url='staff_login')
def edit_staff_profile(request):
    try:
        staff_profile = StaffProfile.objects.get(user=request.user)
        
        if not staff_profile.is_active:
            messages.error(request, 'Your account is not active.')
            logout(request)
            return redirect('staff_login')
        
        if request.method == 'POST':
            form = StaffProfileForm(request.POST, request.FILES, instance=staff_profile)
            if form.is_valid():
                # Update User model fields
                user = request.user
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.email = form.cleaned_data['email']
                user.save()
                
                # Update StaffProfile
                form.save()
                
                request.session['temp_message'] = {
                    'type': 'success',
                    'message': 'Profile updated successfully!'
                }
                request.session.modified = True
                return redirect('staff_dashboard')
            else:
                request.session['temp_message'] = {
                    'type': 'error',
                    'message': 'Error updating profile. Please check the form.'
                }
                request.session.modified = True
        else:
            form = StaffProfileForm(instance=staff_profile)
        
        context = {
            'form': form,
            'staff_profile': staff_profile,
        }
        return render(request, 'cse/staff/edit_profile.html', context)
        
    except StaffProfile.DoesNotExist:
        logout(request)
        messages.error(request, 'You are not registered as staff.')
        return redirect('staff_login')

# Faculty Login System Views
def faculty_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                faculty_member = FacultyMember.objects.get(user=user)
                if faculty_member.status in ['active', 'ex_chairman']:  # Allow active and ex-chairman to login
                    login(request, user)
                    return redirect('faculty_dashboard')
                else:
                    messages.error(request, 'Your account is not active. Please contact the administrator.')
            except FacultyMember.DoesNotExist:
                messages.error(request, 'You are not registered as faculty.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'cse/faculty_and_staff/faculty_login.html')

@login_required
def faculty_logout(request):
    # Clear any pending messages before logout
    if 'dashboard_message' in request.session:
        del request.session['dashboard_message']
    request.session.flush()
    logout(request)
    return redirect('faculty_login')

@login_required(login_url='faculty_login')
def faculty_dashboard(request):
    try:
        faculty_member = FacultyMember.objects.get(user=request.user)
        if faculty_member.status not in ['active', 'ex_chairman']:
            messages.error(request, 'Your account is not active. Please contact the administrator.')
            logout(request)
            return redirect('faculty_login')
        
        # Get faculty's publications and projects
        faculty_publications = Publication.objects.filter(authors__icontains=faculty_member.name).order_by('-publication_date')
        faculty_projects = faculty_member.projects.all().order_by('-start_date')
        
        # Calculate profile completion percentage
        profile_fields = [
            faculty_member.name,
            faculty_member.email,
            faculty_member.phone,
            faculty_member.bio,
            faculty_member.research_interest,
            faculty_member.research_activities,
            faculty_member.publications,
            faculty_member.courses_taught,
            faculty_member.membership,
            faculty_member.awards_honors,
            faculty_member.image.name if faculty_member.image else None,
            faculty_member.cv_file.name if faculty_member.cv_file else None,
        ]
        
        # Add URL fields
        url_fields = [
            faculty_member.research_gate_url,
            faculty_member.google_scholar_url,
            faculty_member.orcid_url,
            faculty_member.linkedin_url,
            faculty_member.personal_website,
        ]
        
        # Count URL fields - consider profile complete if at least 2 URLs are provided
        filled_urls = sum(1 for url in url_fields if url and str(url).strip())
        if filled_urls >= 2:
            profile_fields.append("social_links_sufficient")
        
        # Add education and experience record counts
        education_count = faculty_member.educations.count()
        experience_count = faculty_member.professional_experiences.count()
        
        # Consider education and experience as "filled" if they have any records
        if education_count > 0:
            profile_fields.append("education_records_exist")
        if experience_count > 0:
            profile_fields.append("professional_experience_records_exist")
            
        completed_fields = sum(1 for field in profile_fields if field and str(field).strip())
        profile_completion = int((completed_fields / len(profile_fields)) * 100)
        
        # Get temporary message and remove it from session
        temp_message = None
        if 'temp_message' in request.session:
            temp_message = request.session.pop('temp_message')
            request.session.modified = True

        context = {
            'faculty_member': faculty_member,
            'faculty_publications': faculty_publications,
            'faculty_projects': faculty_projects,
            'profile_completion': profile_completion,
            'current_date': timezone.now(),
            'temp_message': temp_message,
        }
        return render(request, 'cse/faculty_and_staff/faculty_dashboard.html', context)
    except FacultyMember.DoesNotExist:
        logout(request)
        messages.error(request, 'You are not registered as faculty.')
        return redirect('faculty_login')

@login_required(login_url='faculty_login')
def edit_faculty_profile(request):
    try:
        faculty_member = FacultyMember.objects.get(user=request.user)
        
        if request.method == 'POST':
            form = FacultyMemberForm(request.POST, request.FILES, instance=faculty_member)
            if form.is_valid():
                # Save the form but don't change the user field
                updated_faculty = form.save(commit=False)
                updated_faculty.user = request.user  # Ensure user field remains the same
                updated_faculty.save()
                form.save_m2m()  # Save many-to-many relationships if any
                
                messages.success(request, 'Your profile has been updated successfully!')
                return redirect('faculty_dashboard')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = FacultyMemberForm(instance=faculty_member)
        
        context = {
            'form': form,
            'faculty_member': faculty_member,
        }
        return render(request, 'cse/faculty_and_staff/faculty_edit_profile.html', context)
    except FacultyMember.DoesNotExist:
        logout(request)
        messages.error(request, 'You are not registered as faculty.')
        return redirect('faculty_login')

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
    tech_news = TechNews.objects.all().order_by('-published_date')[:3]
    
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

    # Get department statistics for About section
    try:
        stats = DepartmentStatistics.objects.first()
        if not stats:
            stats = DepartmentStatistics.objects.create()
    except Exception:
        stats = None
    
    # Get statistics with auto-calculation for zero values
    if stats:
        total_students = stats.total_students
        total_faculty = stats.get_faculty_count() if stats.total_faculty == 0 else stats.total_faculty
        total_labs = stats.total_labs
        total_research_areas = stats.get_research_areas_count() if stats.total_research_areas == 0 else stats.total_research_areas
        total_publications = stats.get_publications_count() if stats.total_publications == 0 else stats.total_publications
        total_projects = stats.get_projects_count() if stats.total_projects == 0 else stats.total_projects
    else:
        total_students = 150
        total_faculty = FacultyMember.objects.filter(is_current=True, status='active').count()
        total_labs = 3
        total_research_areas = 8
        total_publications = Publication.objects.count()
        total_projects = Project.objects.count()
    
    # Update view count for home page
    page_view, created = ViewCount.objects.get_or_create(page_name='home')
    page_view.increment()
    
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
        # Department statistics for About section
        'total_students': total_students,
        'total_faculty': total_faculty,
        'total_labs': total_labs,
        'total_research_areas': total_research_areas,
        'total_publications': total_publications,
        'total_projects': total_projects,
    }
    
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

#Academis nav bar
def academic_programs(request):
    return render(request, 'cse/academics/academic_programs.html')
def curriculum(request):
    return render(request, 'cse/academics/curriculum.html')
def academic_calendar(request):
    return render(request, 'cse/academics/academic_calendar.html')

#faculty and staff nav bar
def active_faculty(request):
    # Filter by both status='active' and is_current=True, ordered by joined_date (earliest first)
    active_faculty_members = FacultyMember.objects.filter(
        status='active', 
        is_current=True
    ).order_by('joined_date', 'name')
    return render(request, 'cse/faculty_and_staff/active_faculty.html', {
        'faculty_members': active_faculty_members
    })
def ex_chairman(request):
    # Get all ex-chairmen ordered by service start date (who served first appears first)
    ex_chairmen = Chairman.objects.filter(is_current=False).order_by('from_date')
    
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
    return render(request, 'cse/faculty_and_staff/faculty_detail.html', {'faculty': faculty})

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

def all_tech_news(request):
    # Get search query
    query = request.GET.get('q')
    
    # Get all tech news ordered by published date
    news_list = TechNews.objects.all().order_by('-published_date')
    
    # Apply search filter if query exists
    if query:
        news_list = news_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(source__icontains=query)
        )
    
    # Pagination - show 9 items per page
    paginator = Paginator(news_list, 9)
    page = request.GET.get('page')
    
    try:
        tech_news = paginator.page(page)
    except PageNotAnInteger:
        tech_news = paginator.page(1)
    except EmptyPage:
        tech_news = paginator.page(paginator.num_pages)
    
    # Update view count for tech news page
    page_view, created = ViewCount.objects.get_or_create(page_name='tech_news')
    page_view.increment()
    
    return render(request, 'cse/tech_news/all_tech_news.html', {
        'tech_news': tech_news,
        'query': query,
        'is_paginated': tech_news.has_other_pages()
    })

def detail_tech_news(request, pk):
    # Get the specific tech news item
    news = get_object_or_404(TechNews, pk=pk)
    
    # Update view count for this specific tech news
    page_view, created = ViewCount.objects.get_or_create(page_name=f'tech_news_{pk}')
    page_view.increment()
    
    return render(request, 'cse/tech_news/detail_tech_news.html', {'news': news})

def about(request):
    # Update view count for about page
    page_view, created = ViewCount.objects.get_or_create(page_name='about')
    page_view.increment()
    
    # Get or create department statistics
    try:
        stats = DepartmentStatistics.objects.first()
        if not stats:
            # Create default statistics if none exist
            stats = DepartmentStatistics.objects.create()
            print("Created new statistics instance")
        else:
            print(f"Found existing statistics: Students={stats.total_students}, Faculty={stats.total_faculty}")
    except Exception as e:
        # Fallback to default values if model doesn't exist yet
        print(f"Error getting statistics: {e}")
        stats = None
    
    # Get statistics with auto-calculation for zero values
    if stats:
        total_students = stats.total_students
        total_faculty = stats.get_faculty_count() if stats.total_faculty == 0 else stats.total_faculty
        total_labs = stats.total_labs
        total_research_areas = stats.get_research_areas_count() if stats.total_research_areas == 0 else stats.total_research_areas
        total_publications = stats.get_publications_count() if stats.total_publications == 0 else stats.total_publications
        total_projects = stats.get_projects_count() if stats.total_projects == 0 else stats.total_projects
    else:
        # Fallback values
        total_students = 150
        total_faculty = FacultyMember.objects.filter(is_current=True, status='active').count()
        total_labs = 3
        total_research_areas = 8
        total_publications = Publication.objects.count()
        total_projects = Project.objects.count()
    
    print(f"Context values: Students={total_students}, Faculty={total_faculty}, Labs={total_labs}")
    
    context = {
        'total_students': total_students,
        'total_faculty': total_faculty,
        'total_labs': total_labs,
        'total_research_areas': total_research_areas,
        'total_publications': total_publications,
        'total_projects': total_projects,
    }
    
    return render(request, 'cse/about.html', context)

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


# Faculty Education Management Views
@login_required(login_url='faculty_login')
def add_education(request):
    try:
        faculty_member = FacultyMember.objects.get(user=request.user)
        
        if request.method == 'POST':
            form = EducationForm(request.POST)
            if form.is_valid():
                education = form.save(commit=False)
                education.faculty = faculty_member
                education.save()
                messages.success(request, 'Education record added successfully!')
                return redirect('faculty_dashboard')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = EducationForm()
        
        context = {
            'form': form,
            'faculty_member': faculty_member,
            'form_title': 'Add Education Record',
            'form_action': 'Add'
        }
        return render(request, 'cse/faculty_and_staff/manage_education.html', context)
    except FacultyMember.DoesNotExist:
        logout(request)
        messages.error(request, 'You are not registered as faculty.')
        return redirect('faculty_login')


@login_required(login_url='faculty_login')
def edit_education(request, pk):
    try:
        faculty_member = FacultyMember.objects.get(user=request.user)
        education = get_object_or_404(Education, pk=pk, faculty=faculty_member)
        
        if request.method == 'POST':
            form = EducationForm(request.POST, instance=education)
            if form.is_valid():
                form.save()
                messages.success(request, 'Education record updated successfully!')
                return redirect('faculty_dashboard')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = EducationForm(instance=education)
        
        context = {
            'form': form,
            'faculty_member': faculty_member,
            'education': education,
            'form_title': 'Edit Education Record',
            'form_action': 'Update'
        }
        return render(request, 'cse/faculty_and_staff/manage_education.html', context)
    except FacultyMember.DoesNotExist:
        logout(request)
        messages.error(request, 'You are not registered as faculty.')
        return redirect('faculty_login')


@login_required(login_url='faculty_login')
def delete_education(request, pk):
    try:
        faculty_member = FacultyMember.objects.get(user=request.user)
        education = get_object_or_404(Education, pk=pk, faculty=faculty_member)
        
        if request.method == 'POST':
            education.delete()
            messages.success(request, 'Education record deleted successfully!')
            return redirect('faculty_dashboard')
        
        context = {
            'education': education,
            'faculty_member': faculty_member
        }
        return render(request, 'cse/faculty_and_staff/confirm_delete_education.html', context)
    except FacultyMember.DoesNotExist:
        logout(request)
        messages.error(request, 'You are not registered as faculty.')
        return redirect('faculty_login')


# Faculty Professional Experience Management Views
@login_required(login_url='faculty_login')
def add_professional_experience(request):
    try:
        faculty_member = FacultyMember.objects.get(user=request.user)
        
        if request.method == 'POST':
            form = ProfessionalExperienceForm(request.POST)
            if form.is_valid():
                experience = form.save(commit=False)
                experience.faculty = faculty_member
                experience.save()
                messages.success(request, 'Professional experience record added successfully!')
                return redirect('faculty_dashboard')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = ProfessionalExperienceForm()
        
        context = {
            'form': form,
            'faculty_member': faculty_member,
            'form_title': 'Add Professional Experience',
            'form_action': 'Add'
        }
        return render(request, 'cse/faculty_and_staff/manage_experience.html', context)
    except FacultyMember.DoesNotExist:
        logout(request)
        messages.error(request, 'You are not registered as faculty.')
        return redirect('faculty_login')


@login_required(login_url='faculty_login')
def edit_professional_experience(request, pk):
    try:
        faculty_member = FacultyMember.objects.get(user=request.user)
        experience = get_object_or_404(ProfessionalExperience, pk=pk, faculty=faculty_member)
        
        if request.method == 'POST':
            form = ProfessionalExperienceForm(request.POST, instance=experience)
            if form.is_valid():
                form.save()
                messages.success(request, 'Professional experience updated successfully!')
                return redirect('faculty_dashboard')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            form = ProfessionalExperienceForm(instance=experience)
        
        context = {
            'form': form,
            'faculty_member': faculty_member,
            'experience': experience,
            'form_title': 'Edit Professional Experience',
            'form_action': 'Update'
        }
        return render(request, 'cse/faculty_and_staff/manage_experience.html', context)
    except FacultyMember.DoesNotExist:
        logout(request)
        messages.error(request, 'You are not registered as faculty.')
        return redirect('faculty_login')


@login_required(login_url='faculty_login')
def delete_professional_experience(request, pk):
    try:
        faculty_member = FacultyMember.objects.get(user=request.user)
        experience = get_object_or_404(ProfessionalExperience, pk=pk, faculty=faculty_member)
        
        if request.method == 'POST':
            experience.delete()
            messages.success(request, 'Professional experience deleted successfully!')
            return redirect('faculty_dashboard')
        
        context = {
            'experience': experience,
            'faculty_member': faculty_member
        }
        return render(request, 'cse/faculty_and_staff/confirm_delete_experience.html', context)
    except FacultyMember.DoesNotExist:
        logout(request)
        messages.error(request, 'You are not registered as faculty.')
        return redirect('faculty_login')

# Custom 404 Error Handler
def custom_404_view(request, exception=None):
    """
    Custom 404 error handler for all environments.
    Works on production (cse.neu.ac.bd, neu-cse.onrender.com) and development.
    """
    return render(request, 'cse/404.html', status=404)


def fallback_404_view(request, unmatched_path=None):
    """Render the custom 404 template for any unmatched URL when DEBUG=True."""
    return custom_404_view(request)