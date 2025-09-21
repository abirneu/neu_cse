from django import forms
from .models import Notice_Board, ScrollingNotice
from ckeditor.widgets import CKEditorWidget

class NoticeForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Notice_Board
        fields = ['title', 'content', 'file', 'is_important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'is_important': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class ScrollingNoticeForm(forms.ModelForm):
    class Meta:
        model = ScrollingNotice
        fields = ['text', 'is_active']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }