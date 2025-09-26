from django import forms
from .models import Notice_Board, ScrollingNotice, FacultyMember, Education, ProfessionalExperience
from ckeditor.widgets import CKEditorWidget

class NoticeForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Notice_Board
        fields = ['title', 'content', 'file', 'is_important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 rounded-md bg-gray-200 focus:outline-none focus:ring-2 focus:ring-green-500', 'placeholder': 'Enter Notice title'}),
            'file': forms.FileInput(attrs={'class': 'w-full p-2 rounded-md bg-gray-200 focus:outline-none focus:ring-2 focus:ring-green-500'}),
            'is_important': forms.CheckboxInput(attrs={'class': 'h-4 w-4 rounded border-gray-300 text-green-600 focus:ring-green-500'})
        }

class ScrollingNoticeForm(forms.ModelForm):
    class Meta:
        model = ScrollingNotice
        fields = ['text', 'is_active']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'rounded-md bg-gray-200 focus:outline-none focus:ring-2 focus:ring-green-500 p-2', 'rows': 3, 'placeholder': 'Enter scrolling notice text'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class FacultyMemberForm(forms.ModelForm):
    class Meta:
        model = FacultyMember
        fields = [
            'name', 'designation', 'status', 'member_type', 'email', 'phone', 
            'room_no', 'image', 'bio', 'research_interest', 'research_gate_url',
            'google_scholar_url', 'orcid_url', 'linkedin_url', 'personal_website',
            'research_activities', 'publications', 'courses_taught', 'membership', 
            'awards_honors', 'others', 'cv_file', 'joined_date', 'end_date'
        ]
        
        widgets = {
            # Basic Information
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'placeholder': 'Full Name'
            }),
            'designation': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors'
            }),
            'member_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'placeholder': 'Email Address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'placeholder': 'Phone Number'
            }),
            'room_no': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'placeholder': 'Room Number'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'accept': 'image/*'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'rows': 4,
                'placeholder': 'Brief biography...'
            }),
            'research_interest': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'rows': 4,
                'placeholder': 'Research interests and areas of expertise...'
            }),
            
            # URLs
            'research_gate_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'placeholder': 'https://www.researchgate.net/profile/...'
            }),
            'google_scholar_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'placeholder': 'https://scholar.google.com/citations?user=...'
            }),
            'orcid_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'placeholder': 'https://orcid.org/...'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'placeholder': 'https://www.linkedin.com/in/...'
            }),
            'personal_website': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'placeholder': 'https://your-website.com'
            }),
            
            # Rich Text Fields
            'research_activities': CKEditorWidget(),
            'publications': CKEditorWidget(),
            'courses_taught': CKEditorWidget(),
            'membership': CKEditorWidget(),
            'awards_honors': CKEditorWidget(),
            'others': CKEditorWidget(),
            
            # File Upload
            'cv_file': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'accept': '.pdf,.doc,.docx'
            }),
            
            # Dates
            'joined_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'type': 'date'
            }),
        }
        
        labels = {
            'name': 'Full Name',
            'designation': 'Designation',
            'status': 'Current Status',
            'member_type': 'Member Type',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'room_no': 'Room Number',
            'image': 'Profile Photo',
            'bio': 'Biography',
            'research_interest': 'Research Interests',
            'research_gate_url': 'ResearchGate URL',
            'google_scholar_url': 'Google Scholar URL',
            'orcid_url': 'ORCID URL',
            'linkedin_url': 'LinkedIn URL',
            'personal_website': 'Personal Website',
            'research_activities': 'Research Activities',
            'publications': 'Publications',
            'courses_taught': 'Courses Taught',
            'membership': 'Professional Memberships',
            'awards_honors': 'Awards and Honors',
            'others': 'Other Information',
            'cv_file': 'CV/Resume File',
            'joined_date': 'Joining Date',
            'end_date': 'End Date (if applicable)',
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree_name', 'major_subject', 'board_institute', 'country', 'passing_year', 'grade_gpa', 'order']
        
        widgets = {
            'degree_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'placeholder': 'e.g., BSc, MSc, PhD, Diploma'
            }),
            'major_subject': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'placeholder': 'Major Subject/Group'
            }),
            'board_institute': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'placeholder': 'Board/Institute/University name'
            }),
            'country': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'placeholder': 'Country'
            }),
            'passing_year': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'placeholder': 'Year of graduation'
            }),
            'grade_gpa': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'placeholder': 'Grade/GPA/Result (optional)'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'placeholder': '0 for latest'
            }),
        }
        
        labels = {
            'degree_name': 'Degree Name',
            'major_subject': 'Major Subject',
            'board_institute': 'Board/Institute/University',
            'country': 'Country',
            'passing_year': 'Passing Year',
            'grade_gpa': 'Grade/GPA (Optional)',
            'order': 'Order (0 for latest)',
        }


class ProfessionalExperienceForm(forms.ModelForm):
    class Meta:
        model = ProfessionalExperience
        fields = ['position_title', 'organization', 'location', 'start_date', 'end_date', 'is_current', 'description', 'order']
        
        widgets = {
            'position_title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'placeholder': 'Job title/position'
            }),
            'organization': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'placeholder': 'Organization/Company name'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'placeholder': 'Location (City, Country)'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'type': 'date'
            }),
            'is_current': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-custom-green focus:ring-custom-green border-gray-300 rounded'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'rows': 4,
                'placeholder': 'Job description/responsibilities'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-custom-green focus:border-custom-green transition-colors',
                'placeholder': '0 for latest'
            }),
        }
        
        labels = {
            'position_title': 'Position Title',
            'organization': 'Organization',
            'location': 'Location',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'is_current': 'Currently working here',
            'description': 'Job Description',
            'order': 'Order (0 for latest)',
        }