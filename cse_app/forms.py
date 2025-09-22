from django import forms
from .models import Notice_Board, ScrollingNotice
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