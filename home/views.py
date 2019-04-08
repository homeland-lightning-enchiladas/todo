from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Task, Profile
from .forms import AddTaskForm, UserCreationForm
from django.shortcuts import redirect

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        tasks = user_profile.tasks.filter(is_complete=False)
        completed_tasks = user_profile.tasks.filter(is_complete=True)
    else:
        tasks = None
        completed_tasks = None

    if request.method == 'POST':
        form = AddTaskForm(request.POST)

        if form.is_valid():
            description = form.cleaned_data['description']
            task = Task.objects.create_task(description, user_profile)
            task.save()

            return HttpResponseRedirect('/')
    
    else:
        form = AddTaskForm()

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

def not_complete_task(request, id):
    task = Task.objects.get(id=id)
    task.is_complete = False
    task.save(update_fields=['is_complete'])
    return HttpResponseRedirect('/')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register_success')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def register_success(request):
    return render(request, 'registration/register_success.html')
