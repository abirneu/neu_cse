# Faculty Profile Edit System - Usage Guide

## Overview
The faculty profile edit system allows faculty members to update their complete profile information through a user-friendly web interface.

## Features

### 📝 **Complete Profile Management**
- **Basic Information:** Name, designation, status, email, phone, room number
- **Academic URLs:** ResearchGate, Google Scholar, ORCID, LinkedIn, personal website  
- **Rich Text Content:** Education, professional experience, research activities, publications, courses taught
- **Achievements:** Professional memberships, awards and honors
- **Files:** Profile photo, CV/Resume upload
- **Dates:** Joining date, end date management

### 🎨 **User Experience**
- **Professional Design:** Tailwind CSS styling with consistent branding
- **Responsive Layout:** Works on desktop, tablet, and mobile devices
- **Form Validation:** Client-side and server-side validation
- **File Previews:** Image preview for profile photos
- **Rich Text Editing:** CKEditor for formatted content
- **Auto-save URLs:** Automatically adds https:// to social links

### 🔐 **Security Features**
- **Login Required:** Only authenticated faculty can edit profiles
- **User Verification:** Ensures faculty can only edit their own profile
- **File Type Validation:** Restricts uploads to appropriate file types
- **CSRF Protection:** Django built-in CSRF protection

## How to Use

### For Faculty Members:

1. **Login to Faculty Portal:**
   - Click "Faculty Login" button in the website footer
   - Enter your username and password
   - You'll be redirected to your faculty dashboard

2. **Access Profile Edit:**
   - From the dashboard, click "Edit Profile" button in the profile card
   - OR click "Update Profile" in the Quick Actions section

3. **Update Your Information:**
   - Fill out the comprehensive form with your information
   - Upload new profile photo if needed
   - Add/update your academic URLs
   - Update your CV/Resume file
   - Use the rich text editor for detailed sections

4. **Save Changes:**
   - Click "Update Profile" button at the bottom
   - You'll see a success message and return to the dashboard
   - Your changes are immediately visible on your public profile

### For Administrators:

1. **Create Faculty User Accounts:**
   ```bash
   # List all faculty and their user status
   python manage.py create_faculty_users --list
   
   # Create user account for specific faculty member
   python manage.py create_faculty_users --faculty-id 1
   
   # Create user accounts for all faculty members
   python manage.py create_faculty_users --all
   ```

2. **Default Login Credentials:**
   - **Username:** Auto-generated from faculty name (e.g., "abdullahas" for "Abdullah Al Shiam")
   - **Password:** `faculty123` (faculty should change this after first login)

3. **Access URLs:**
   - Faculty Login: `http://your-domain/faculty/login/`
   - Faculty Dashboard: `http://your-domain/faculty/dashboard/`
   - Profile Edit: `http://your-domain/faculty/edit-profile/`

## Form Fields Reference

### Basic Information Section
- **Full Name** - Faculty member's complete name
- **Designation** - Professor, Associate Professor, Assistant Professor, Lecturer, Chairman
- **Current Status** - Active, On Leave, Ex-Chairman, Past Faculty
- **Member Type** - Full-time, Part-time, Visiting, Adjunct
- **Email Address** - Official email contact
- **Phone Number** - Contact phone number
- **Room Number** - Office room location
- **Joining Date** - Date of joining the department
- **Profile Photo** - Professional headshot image
- **Biography** - Brief personal and professional bio
- **Research Interests** - Areas of research expertise

### Academic & Social Links Section
- **ResearchGate URL** - ResearchGate profile link
- **Google Scholar URL** - Google Scholar citations profile
- **ORCID URL** - ORCID researcher identifier
- **LinkedIn URL** - Professional LinkedIn profile
- **Personal Website** - Personal or academic website

### Academic Information Section
- **Educational Background** - Academic qualifications and degrees
- **Professional Experience** - Career history and positions
- **Research Activities** - Current and past research projects
- **Publications** - List of academic publications
- **Courses Taught** - Subjects and courses taught

### Achievements & Memberships Section
- **Professional Memberships** - Academic and professional organization memberships
- **Awards and Honors** - Recognition and achievements received
- **Other Information** - Additional relevant information

### Documents & Files Section
- **CV/Resume File** - Upload PDF, DOC, or DOCX files
- **End Date** - Only for faculty who are no longer active

## Technical Implementation

### Files Created/Modified:
1. **Forms:** `cse_app/forms.py` - Added `FacultyMemberForm`
2. **Views:** `cse_app/views.py` - Added `edit_faculty_profile` view
3. **Templates:** `templates/cse/faculty_and_staff/faculty_edit_profile.html`
4. **URLs:** `cse_app/urls.py` - Added `/faculty/edit-profile/` route
5. **Dashboard:** Updated faculty dashboard with edit links

### Database Fields:
All existing FacultyMember model fields are editable except:
- `user` - Relationship to User model (protected)
- `id` - Primary key (auto-generated)
- `is_chairman` - Administrative flag (admin only)

### Security Measures:
- Login required for all faculty operations
- User can only edit their own profile
- CSRF token protection
- File upload restrictions
- Form validation on client and server side

## Troubleshooting

### Common Issues:

1. **"You are not registered as faculty" error:**
   - Ensure faculty member has a linked user account
   - Use management command to create user account

2. **Profile photo not uploading:**
   - Check file size (should be reasonable)
   - Ensure file is an image format (JPG, PNG, GIF)
   - Check media file permissions

3. **Rich text editor not loading:**
   - Ensure CKEditor is properly installed
   - Check browser console for JavaScript errors

4. **Form validation errors:**
   - Check required fields are filled
   - Ensure email format is valid
   - Check URL formats for social links

### Support:
For technical issues or questions about the faculty profile system, contact the system administrator or development team.