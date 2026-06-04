from django.urls import path
from . import views

urlpatterns = [
    path('', views.habit_list, name='habit_list'),
    path('create/', views.habit_create, name='habit_create'),
    path('<int:habit_id>/done/', views.habit_done, name='habit_done'),
    path('<int:habit_id>/delete/', views.habit_delete, name='habit_delete'),
]