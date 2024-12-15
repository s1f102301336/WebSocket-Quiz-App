from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_create, name='quiz_create'),
    path('makequiz', views.makequiz, name='makequiz')
]