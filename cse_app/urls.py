from django.urls import path
from . import views
from .test_views import test_faculty_form

urlpatterns = [
    # Test URL
    path('test-faculty-form/', test_faculty_form, name='test_faculty_form'),
    
    # Staff URLs
    path('staff/login/', views.staff_login, name='staff_login'),
    path('staff/logout/', views.staff_logout, name='staff_logout'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/create-notice/', views.create_notice, name='create_notice'),
    path('staff/edit-notice/<int:pk>/', views.edit_notice, name='edit_notice'),
    path('staff/delete-notice/<int:pk>/', views.delete_notice, name='delete_notice'),
    path('staff/create-scrolling-notice/', views.create_scrolling_notice, name='create_scrolling_notice'),
    path('staff/edit-scrolling-notice/<int:pk>/', views.edit_scrolling_notice, name='edit_scrolling_notice'),
    path('staff/delete-scrolling-notice/<int:pk>/', views.delete_scrolling_notice, name='delete_scrolling_notice'),
    
   
    
    # Faculty URLs
    path('faculty/login/', views.faculty_login, name='faculty_login'),
    path('faculty/logout/', views.faculty_logout, name='faculty_logout'),
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    
    # Faculty URLs
    path('faculty/login/', views.faculty_login, name='faculty_login'),
    path('faculty/logout/', views.faculty_logout, name='faculty_logout'),
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('faculty/edit-profile/', views.edit_faculty_profile, name='edit_faculty_profile'),
    
    # Faculty Education Management
    path('faculty/education/add/', views.add_education, name='add_education'),
    path('faculty/education/edit/<int:pk>/', views.edit_education, name='edit_education'),
    path('faculty/education/delete/<int:pk>/', views.delete_education, name='delete_education'),
    
    # Faculty Professional Experience Management
    path('faculty/experience/add/', views.add_professional_experience, name='add_professional_experience'),
    path('faculty/experience/edit/<int:pk>/', views.edit_professional_experience, name='edit_professional_experience'),
    path('faculty/experience/delete/<int:pk>/', views.delete_professional_experience, name='delete_professional_experience'),
    
    path('', views.home, name='home'),
    path('notices/', views.notice_list, name='notice_list'),
    path('notices/<int:pk>/', views.notice_detail, name='notice_detail'),
    path('notices/<int:pk>/download/', views.download_notice, name='download_notice'),
    path('notices/<int:pk>/view/', views.view_notice_file, name='view_notice_file'),
    path('faculty/', views.faculty_list, name='faculty_list'),
    path('faculty/<int:pk>/', views.faculty_detail, name='faculty_detail'),
    path('chairman/', views.chairman_message, name='chairman_message'),
    
    path('publications/', views.publications_home, name='publications_home'),
    path('publications/all/', views.all_publications, name='all_publications'),
    path('publications/<int:pk>/', views.publication_detail, name='publication_detail'),
    
    path('projects/', views.projects, name='projects'),
    path('projects/all/', views.all_projects, name='all_projects'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('tech-news/', views.all_tech_news, name='all_tech_news'),
    path('tech-news/<int:pk>/', views.detail_tech_news, name='detail_tech_news'),
    path('about/', views.about, name='about'),
    path('events/', views.events, name='events'),
    path('events/all/', views.all_events, name='all_events'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    
    #About URLs
    path('why-neu-cse/', views.why_neu_cse, name='why_neu_cse'),
    path('message-from-department/', views.message_from_department, name='message_from_department'),
    path('message-from-chairman/', views.message_from_chairman, name='message_from_chairman'),
    path('facilities/', views.facilities, name='facilities'),
    path('history-neu-cse/', views.history_neu_cse, name='history_neu_cse'),
    path('mission-vision/', views.mission_vision, name='mission_vision'),
    path('history-neu/', views.history_neu, name='history_neu'),
    path('achievements/', views.achievements, name='achievements'),
    
    # Academics URLs
    path('academics/', views.academic_programs, name='academic_programs'),
    path('curriculum/', views.curriculum, name='curriculum'),
    path('academic-calendar/', views.academic_calendar, name='academic_calendar'),
    
    path('faculty/active/', views.active_faculty, name='active_faculty'),
    path('faculty/ex-chairman/', views.ex_chairman, name='ex_chairman'),
    path('faculty/on-leave/', views.faculty_on_leave, name='faculty_on_leave'),
    path('faculty/past/', views.past_faculty, name='past_faculty'),
    path('faculty/officer-and-staff/', views.officer_and_staff, name='officer_and_staff'),

    path('alumni/', views.alumni, name='alumni'),

    path('clubs/computer/', views.computer_club, name='computer_club'),
    path('clubs/programming/', views.programming_club, name='programming_club'),

    path('contact-us/', views.contact_us, name='contact_us'),
    # Image Gallery URLs
    path('gallery/', views.image_gallery_home, name='image_gallery_home'),
    path('gallery/all/', views.all_images, name='all_images'),

    
]