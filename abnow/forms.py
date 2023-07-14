# forms.py
from django import forms
from .models import Image, Code, CodeCategory, SubCode

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['filename', 'uploader', 'image', 'codes', 'sub_codes']

class CodeForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = ['name', 'category']

class CodeCategoryForm(forms.ModelForm):
    class Meta:
        model = CodeCategory
        fields = ['name']

class SubCodeForm(forms.ModelForm):
    class Meta:
        model = SubCode
        fields = ['name', 'code']

class SearchForm(forms.Form):
    q = forms.CharField()