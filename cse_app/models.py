from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField  # For rich text content

# Create your models here.
class Notice_Board(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    file = models.FileField(upload_to='notices/', blank=True, null=True)  # For download option
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_important = models.BooleanField(default=False)


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
    end_date = models.DateField(blank=True, null=True)
    is_ongoing = models.BooleanField(default=False)
    funding_agency = models.CharField(max_length=200, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    outcome = RichTextField(blank=True)
    
    def __str__(self):
        return self.title


class FacultyMember(models.Model):
    DESIGNATION_CHOICES = (
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('assistant_professor', 'Assistant Professor'),
        ('lecturer', 'Lecturer'),
        ('chairman', 'Chairman'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=30, choices=DESIGNATION_CHOICES)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    room_no = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to='faculty/', blank=True)
    bio = models.TextField(blank=True)
    education = RichTextField(blank=True)
    research_interest = models.TextField(blank=True)
    joined_date = models.DateField(blank=True, null=True)
    is_chairman = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['joined_date']


class Chairman(models.Model):
    faculty = models.OneToOneField(FacultyMember, on_delete=models.CASCADE)
    message = RichTextField()
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