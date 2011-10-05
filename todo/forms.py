from django import forms
from django.core.validators import RegexValidator

class DeleteListForm(forms.Form):
   id = forms.CharField(max_length=128, min_length=1, required=True, validators=[RegexValidator(r'^\d+$')])

class CreateListForm(forms.Form):
   name = forms.CharField(max_length=128, min_length=1, required=True)

class EditListForm(forms.Form):
    id = forms.CharField(max_length=128, min_length=1, required=True, validators=[RegexValidator(r'^\d+$')])
    name = forms.CharField(max_length=128, min_length=1, required=True)


class CreateItemForm(forms.Form):
    text = forms.CharField(max_length=256, min_length=1, required=True, widget=forms.Textarea({'rows':3}))
    due_on = forms.DateTimeField(
        required=False,
        input_formats=('%b %d, %Y %H:%M %p',),
        widget=forms.DateTimeInput(format='%b %d, %Y %H:%M %p')
    )

    started_on = forms.DateTimeField(
        required=False,
        input_formats=('%b %d, %Y %H:%M %p',),
        widget=forms.DateTimeInput(format='%b %d, %Y %H:%M %p')
    )
    
    priority = forms.ChoiceField(required=False,
        choices=(
                (None, 'No priority'),
                ('A', 'Urgent and Important'),
                ('B', 'Important but Not Urgent'),
                ('C', 'Neither Urgent nor Important')
            )
    )
    completed = forms.BooleanField(required=False)
