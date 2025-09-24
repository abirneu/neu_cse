from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField  # For rich text content

# Create your models here.
class ScrollingNotice(models.Model):
    text = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.text[:50]

    class Meta:
        ordering = ['-created_at']

class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20, unique=True)
    designation = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    profile_image = models.ImageField(upload_to='staff/profiles/', null=True, blank=True)
    join_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.staff_id}"

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

class Notice_Board(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    file = models.FileField(upload_to='notices/', blank=True, null=True)  # For download option
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_important = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  # Newest first
class Publication(models.Model):
    PUBLICATION_TYPES = (
        ('journal', 'Journal Article'),
        ('conference', 'Conference Paper'),
        ('book', 'Book'),
        ('chapter', 'Book Chapter'),
    )
    
    title = models.CharField(max_length=300)
    authors = models.CharField(max_length=500)
    publication_type = models.CharField(max_length=20, choices=PUBLICATION_TYPES)
    journal_or_conference_name = models.CharField(max_length=200, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    publication_date = models.DateField()
    doi = models.CharField(max_length=100, blank=True)
    link = models.URLField(blank=True)
    abstract = models.TextField(blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publication_date']


class Project(models.Model):
    PROJECT_TYPES = (
        ('research', 'Research Project'),
        ('thesis', 'Thesis Project'),
        ('industry', 'Industry Project'),
        ('academic', 'Academic Project'),
    )
    
    title = models.CharField(max_length=200)
    description = RichTextField()
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES)
    members = models.ManyToManyField('FacultyMember', related_name='projects', blank=True)
    start_date = models.DateField()
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_ongoing = models.BooleanField(default=False)
    funding_agency = models.CharField(max_length=200, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    outcome = RichTextField(blank=True)
    
    def __str__(self):
        return self.title


class Education(models.Model):
    faculty = models.ForeignKey('FacultyMember', on_delete=models.CASCADE, related_name='educations')
    degree_name = models.CharField(max_length=200, help_text="e.g., BSc, MSc, PhD, Diploma")
    major_subject = models.CharField(max_length=200, help_text="Group/Major Subject")
    board_institute = models.CharField(max_length=200, help_text="Board/Institute/University name")
    country = models.CharField(max_length=100, default="Bangladesh")
    passing_year = models.IntegerField(help_text="Year of graduation/completion")
    grade_gpa = models.CharField(max_length=50, blank=True, help_text="Grade/GPA/Result (optional)")
    order = models.IntegerField(default=0, help_text="Order for display (0 for latest)")
    
    def __str__(self):
        return f"{self.faculty.name} - {self.degree_name}"
    
    class Meta:
        ordering = ['order', '-passing_year']
        verbose_name = 'Education'
        verbose_name_plural = 'Education Records'


class FacultyMember(models.Model):
    DESIGNATION_CHOICES = (
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('assistant_professor', 'Assistant Professor'),
        ('lecturer', 'Lecturer'),
        ('chairman', 'Chairman'),
    )
    
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('ex_chairman', 'Ex-Chairman'),
        ('past_faculty', 'Past Faculty'),
    )

    MEMBER_TYPE_CHOICES = (
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('visiting', 'Visiting'),
        ('adjunct', 'Adjunct'),
    )
    
    # Basic Information
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=30, choices=DESIGNATION_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    member_type = models.CharField(max_length=20, choices=MEMBER_TYPE_CHOICES, default='full_time')
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    room_no = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to='faculty/', blank=True)
    bio = models.TextField(blank=True)
    
    # Research and Academic Information
    research_interest = models.TextField(blank=True)
    research_gate_url = models.URLField(blank=True, help_text="ResearchGate profile URL")
    google_scholar_url = models.URLField(blank=True, help_text="Google Scholar profile URL")
    orcid_url = models.URLField(blank=True, help_text="ORCID profile URL")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")
    personal_website = models.URLField(blank=True, help_text="Personal website URL")
    
    # Education and Professional Experience
    education = RichTextField(blank=True, help_text="Educational background")
    professional_experience = RichTextField(blank=True, help_text="Professional experience")
    research_activities = RichTextField(blank=True, help_text="Research activities and projects")
    
    # Publications and Courses
    publications = RichTextField(blank=True, help_text="List of publications")
    courses_taught = RichTextField(blank=True, help_text="Courses taught")
    
    # Memberships and Awards
    membership = RichTextField(blank=True, help_text="Professional memberships")
    awards_honors = RichTextField(blank=True, help_text="Awards and honors received")
    
    # Other Information
    others = RichTextField(blank=True, help_text="Other relevant information")
    cv_file = models.FileField(upload_to='faculty/cv/', blank=True, null=True, help_text="Upload CV/Resume")
    
    # Administrative Information
    joined_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_chairman = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.get_designation_display()}"

    class Meta:
        ordering = ['designation', 'name']
        verbose_name = 'Faculty Member'
        verbose_name_plural = 'Faculty Members'

class CarouselItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='carousel/')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

class Staff(models.Model):
    STAFF_TYPE_CHOICES = (
        ('officer', 'Officer'),
        ('staff', 'Staff'),
    )
    
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('past_staff', 'Past Staff'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    staff_type = models.CharField(max_length=20, choices=STAFF_TYPE_CHOICES)
    designation = models.CharField(max_length=100)  # Free text field for designation
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    room_no = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to='staff/', blank=True)
    bio = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    joined_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} - {self.get_staff_type_display()} ({self.designation})"
    
    class Meta:
        ordering = ['staff_type', 'name']
        verbose_name_plural = 'Staff'
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['joined_date']


class Chairman(models.Model):
    faculty = models.OneToOneField(FacultyMember, on_delete=models.CASCADE)
    message = RichTextField()
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)
    from_date = models.DateField()
    to_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.is_current:
            # Set all other chairmen to not current
            Chairman.objects.filter(is_current=True).update(is_current=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.faculty.name} - {'Current' if self.is_current else 'Former'} Chairman"
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Chairman: {self.faculty.name}"


class TechNews(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    source = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True)
    published_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='tech_news/', blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Tech News"
        ordering = ['-published_date']


class ViewCount(models.Model):
    page_name = models.CharField(max_length=100, unique=True)
    count = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.page_name}: {self.count} views"

    def increment(self):
        self.count += 1
        self.save()
        
class Event(models.Model):
    EVENT_TYPES = (
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('webinar', 'Webinar'),
        ('competition', 'Competition'),
        ('programming_contest', 'Programming Contest'),
        ('hackathon', 'Hackathon'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=200)
    description = RichTextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    organizer = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    registration_link = models.URLField(blank=True)
    is_upcoming = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Automatically update is_upcoming based on end_date
        if self.end_date < timezone.now():
            self.is_upcoming = False
        else:
            self.is_upcoming = True
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['start_date']
        
class ImageGallery(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-upload_time']
        verbose_name_plural = 'Image Gallery'

from django.utils import timezone


class ComputerClubMember(models.Model):
    POSITION_CHOICES = [
        # High Priority (Core Leadership)
        ('president', 'President'),
        ('vice_president', 'Vice President'),
        ('general_secretary', 'General Secretary'),
        ('assistant_general_secretary', 'Assistant General Secretary'),
        ('treasurer', 'Treasurer'),
        
        # Mid Priority (Key Operations)
        ('editor_secretary', 'Editor Secretary'),
        ('programming_secretary', 'Programming Secretary'),
        ('assistant_programming_secretary', 'Assistant Programming Secretary'),
        ('sports_secretary', 'Sports Secretary'),
        ('assistant_sports_secretary', 'Assistant Sports Secretary'),
        ('event_management_secretary', 'Event Management Secretary'),
        
        # Support / Communication Roles
        ('publicity_secretary', 'Publicity & Publication Secretary'),
        ('assistant_publicity_secretary', 'Assistant Publicity & Publication Secretary'),
        ('assistant_information_secretary', 'Assistant Information Secretary'),
        ('assistant_organizing_secretary', 'Assistant Organizing Secretary'),
    ]

    PRIORITY_LEVELS = {
        'president': 1,
        'vice_president': 1,
        'general_secretary': 1,
        'assistant_general_secretary': 1,
        'treasurer': 1,
        'editor_secretary': 2,
        'programming_secretary': 2,
        'assistant_programming_secretary': 2,
        'sports_secretary': 2,
        'assistant_sports_secretary': 2,
        'event_management_secretary': 2,
        'publicity_secretary': 3,
        'assistant_publicity_secretary': 3,
        'assistant_information_secretary': 3,
        'assistant_organizing_secretary': 3,
    }

    name = models.CharField(max_length=100)
    session = models.CharField(max_length=20)
    image = models.ImageField(upload_to='club/computer_club/', blank=True, null=True)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)

    class Meta:
        ordering = ['position']
        verbose_name = 'Computer Club Member'
        verbose_name_plural = 'Computer Club Members'

    def get_priority_level(self):
        return self.PRIORITY_LEVELS.get(self.position, 999)

    def __str__(self):
        return f"{self.name} - {self.get_position_display()}"
