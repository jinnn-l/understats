from django import forms
from .choices import *

class UploadFileForm(forms.Form):
    test = forms.ChoiceField(choices = STATISTICAL_TESTS_CHOICES)
    file = forms.FileField(label = 'File Upload')