from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('new/', views.task_create, name='task_create'),
    path('edit/<int:pk>/', views.update_task, name='update_task'),
    path('update_task_progress/', views.update_task_progress, name='update_task_progress'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('reset_task/<int:task_id>/', views.reset_task, name='reset_task'),
    path('history/', views.task_history, name='task_history'),
    path('complete_task/', views.complete_task, name='complete_task'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
]
