from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/delete/', views.delete_task, name='task_delete'),
    path('<int:id>/complete/', views.complete_task, name='task_complete'),
    path('<int:id>/not-complete/', views.not_complete_task, name='task_not_complete'),
    path('register/', views.register, name='register'),
    path('register_success/', views.register_success, name='register_success'),
]