from django import forms
from django.core.validators import RegexValidator

class ListForm(forms.Form):
   name = forms.CharField(max_length=128, min_length=3, required=True)

class ItemForm(forms.Form):
   text = forms.CharField(max_length=128, min_length=3, required=True)
   due_on = forms.DateTimeField(required=False)
   started_on = forms.DateTimeField(required=False)
   priority = forms.ChoiceField(choices=(
               ('A', 'Urgent and Important'),
               ('B', 'Important but Not Urgent'),
               ('C', 'Neither Urgent nor Important')
           ), required=False)
   
   completed = forms.BooleanField(required=False)
