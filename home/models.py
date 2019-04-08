from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class TaskManager(models.Manager):
    def create_task(self, description, creator):
        task = creator.tasks.create(description=description, creator=creator)
        return task
class Task(models.Model):
    description = models.CharField(max_length=300)
    is_complete = models.BooleanField(default=False)
    creator = models.ForeignKey("Profile", on_delete=models.CASCADE)

    objects = TaskManager()

    def __str__(self):
        return self.description

class Team(models.Model):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField("Profile")

    def __str__(self):
        return self.name

# Extension of default Django User class for storing
# each user's tasks
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tasks = models.ManyToManyField("Task")

    def __str__(self):
        return self.user.username

# Basically we are hooking the create_user_profile and save_user_profile methods to the User model, 
# whenever a save event occurs. This kind of signal is called post_save.
# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
