from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(max_length=10)


class CreateEntryForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)
