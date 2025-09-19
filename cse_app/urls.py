from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('notices/', views.notice_list, name='notice_list'),
    path('notices/<int:pk>/', views.notice_detail, name='notice_detail'),
    path('notices/<int:pk>/download/', views.download_notice, name='download_notice'),
    path('notices/<int:pk>/view/', views.view_notice_file, name='view_notice_file'),
    path('faculty/', views.faculty_list, name='faculty_list'),
    path('faculty/<int:pk>/', views.faculty_detail, name='faculty_detail'),
    path('chairman/', views.chairman_message, name='chairman_message'),
    path('publications/', views.publications, name='publications'),
    path('projects/', views.projects, name='projects'),
    path('projects/all/', views.all_projects, name='all_projects'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('tech-news/', views.tech_news, name='tech_news'),
    path('about/', views.about, name='about'),
    path('events/', views.events, name='events'),
    path('events/all/', views.all_events, name='all_events'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('why-neu-cse/', views.why_neu_cse, name='why_neu_cse'),
    path('message-from-department/', views.message_from_department, name='message_from_department'),
    path('message-from-chairman/', views.message_from_chairman, name='message_from_chairman'),
    path('facilities/', views.facilities, name='facilities'),
    path('history-neu-cse/', views.history_neu_cse, name='history_neu_cse'),
    path('mission-vision/', views.mission_vision, name='mission_vision'),
    path('history-neu/', views.history_neu, name='history_neu'),
    path('achievements/', views.achievements, name='achievements'),
    
    path('faculty/active/', views.active_faculty, name='active_faculty'),
    path('faculty/ex-chairman/', views.ex_chairman, name='ex_chairman'),
    path('faculty/on-leave/', views.faculty_on_leave, name='faculty_on_leave'),
    path('faculty/past/', views.past_faculty, name='past_faculty'),
    path('faculty/officer-and-staff/', views.officer_and_staff, name='officer_and_staff'),

    path('alumni/', views.alumni, name='alumni'),

    path('clubs/computer/', views.computer_club, name='computer_club'),
    path('clubs/programming/', views.programming_club, name='programming_club'),

    path('contact-us/', views.contact_us, name='contact_us'),
    
]