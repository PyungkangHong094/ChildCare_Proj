from django import forms
from .models import Application

class ApplicationForm(forms.Form):
    attached_file = forms.FileField(label='Select a file')
    title = forms.CharField(max_length=80, error_messages={'required': 'Please enter your title'}, widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'title', 'row':'1'}))
    content = forms.CharField(label='content', widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'content', 'row':'4'}))
    
    class Meta:
        model = Application
        fields = ('title','content','attached_file')
        