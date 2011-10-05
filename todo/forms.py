from django import forms
from django.core.validators import RegexValidator

class DeleteListForm(forms.Form):
   id = forms.CharField(max_length=128, min_length=1, required=True, validators=[RegexValidator(r'^\d+$')])

class CreateListForm(forms.Form):
   name = forms.CharField(max_length=128, min_length=1, required=True)

class EditListForm(forms.Form):
    id = forms.CharField(max_length=128, min_length=1, required=True, validators=[RegexValidator(r'^\d+$')])
    name = forms.CharField(max_length=128, min_length=1, required=True)
