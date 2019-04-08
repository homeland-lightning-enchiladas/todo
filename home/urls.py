from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/delete/', views.delete_task, name='task_delete'),
    path('<int:id>/complete/', views.complete_task, name='task_complete')
]