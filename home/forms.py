from django import forms
from django.core.exceptions import ValidationError

class AddTaskForm(forms.Form):
    description = forms.CharField(max_length=300, required=True)

    # def clean_description(self):
    #     data = self.cleaned_data['description']

    #     if len(data) > 300:
    #         raise ValidationError('Task description too long')
        
    #     return data