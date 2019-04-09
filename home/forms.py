from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Task, Profile

class AddTaskForm(forms.Form):
    description = forms.CharField(max_length=300, required=True)

    def clean_description(self):
        data = self.cleaned_data['description']
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

class ReassignTaskForm(forms.Form):
    id = forms.IntegerField(required=True, widget= forms.TextInput(attrs={'readonly': 'readonly'}))
    email = forms.EmailField(required=True)

    def clean_id(self):
        task_id = self.cleaned_data['id']
        tasks = Task.objects.filter(id=task_id)
        if tasks.count() != 1:
            raise ValidationError('Invalid Task ID')
        return task_id
    
    def clean_email(self):
        email = self.cleaned_data['email']
        users = Profile.objects.filter(user__email=email)
        if users.count() == 0:
            raise ValidationError('User with that email was not found')
        elif users.count() > 1:
            raise ValidationError('There are multiple users with that email')
        return email
