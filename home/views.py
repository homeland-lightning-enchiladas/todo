from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Task, Profile
from .forms import AddTaskForm

# Create your views here.

def index(request):
    user_profile = Profile.objects.get(user__id=3)

    if request.method == 'POST':
        form = AddTaskForm(request.POST)

        if form.is_valid():
            description = form.cleaned_data['description']
            task = Task.objects.create_task(description, user_profile)
            task.save()

            return HttpResponseRedirect('/')
    
    else:
        form = AddTaskForm()

    
    tasks = user_profile.tasks.filter(is_complete=False)
    completed_tasks = user_profile.tasks.filter(is_complete=True)

    context = {
        'form': form,
        'tasks': tasks,
        'completed_tasks': completed_tasks,
    }

    return render(request, 'index.html', context)

# TODO: require login
def delete_task(request, id):
    Task.objects.get(id=id).delete()
    return HttpResponseRedirect('/')

def complete_task(request, id):
    task = Task.objects.get(id=id)
    task.is_complete = True
    task.save(update_fields=['is_complete'])
    return HttpResponseRedirect('/')
