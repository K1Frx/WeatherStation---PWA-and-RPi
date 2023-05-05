from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('all/', views.all),
    path('about/', views.about),
    path('graphs/', views.graphs),
]