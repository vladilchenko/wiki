from django import forms
from . import util

def validate_title(title):
    if title in util.list_entries():
        raise forms.ValidationError("Title already exists")


class SearchForm(forms.Form):
    query = forms.CharField(max_length=10)


class CreateEntryForm(forms.Form):
    title = forms.CharField(max_length=100, validators=[validate_title])
    content = forms.CharField(widget=forms.Textarea)


class EditEntryForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)
