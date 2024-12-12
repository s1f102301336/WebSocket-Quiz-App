from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('answerquiz', views.answerquiz, name='answerquiz'),
    path('makequiz', views.makequiz, name='makequiz'),
]