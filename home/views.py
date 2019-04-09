from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Task, Profile
from .forms import AddTaskForm, UserCreationForm, ReassignTaskForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.messages import get_messages

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        user_profile = Profile.objects.get(user=request.user)
        tasks = user_profile.tasks.filter(is_complete=False)
        completed_tasks = user_profile.tasks.filter(is_complete=True)
    else:
        tasks = None
        completed_tasks = None
    
    # If True, modal will appear. Used for error validation on Reassign Task Form
    show_reassign_modal = False
    old_task_id = ''

    if request.method == 'POST':
        if 'add-task' in request.POST:
            add_task_form = AddTaskForm(request.POST)

            if add_task_form.is_valid():
                description = add_task_form.cleaned_data['description']
                task = Task.objects.create_task(description, user_profile)
                task.save()
            
            reassign_form = ReassignTaskForm()

        elif 'reassign-task' in request.POST:
            reassign_form = ReassignTaskForm(request.POST)
            if reassign_form.is_valid():
                task_id = reassign_form.cleaned_data['id']
                reassign_email = reassign_form.cleaned_data['email']

                ### Reassign Task logic ###
                task = Task.objects.get(id=task_id)
                # Remove associtation with current Profile
                user_profile.tasks.remove(task)
                # Get new profile
                new_profile = Profile.objects.get(user__email=reassign_email)
                # Create association with new user
                new_profile.tasks.add(task)
                # Save
                task.save()
                new_profile.save()

                # Send successful Django message
                messages.add_message(request, messages.INFO, f'Task {task_id} reassigned to {reassign_email}')
            else:
                show_reassign_modal = True
                old_task_id = reassign_form.data['id']
            
            add_task_form = AddTaskForm()
    else:
        add_task_form = AddTaskForm()
        reassign_form = ReassignTaskForm()

    context = {
        'form': add_task_form,
        'reassign_form': reassign_form,
        'tasks': tasks,
        'completed_tasks': completed_tasks,
        'messages': get_messages(request),
        'show_reassign_modal': show_reassign_modal,
        'old_task_id': old_task_id,
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
