from django.urls import path
from . import views

urlpatterns = [
    path('', views.answerquiz, name='answerquiz'),
]