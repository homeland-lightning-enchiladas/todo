from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AddTaskForm(forms.Form):
    description = forms.CharField(max_length=300, required=True)

    def clean_description(self):
        data = self.cleaned_data['description']
        print('DATA LENGTH', len(data))

        if len(data) >= 300:
            raise ValidationError('Task description too long')
        
        return data

class UserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(label="Email address", required=True, help_text="Required")
    

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("That user is already taken")
        return username

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.username = self.clean_username()
        if commit:
            user.save()
        return user