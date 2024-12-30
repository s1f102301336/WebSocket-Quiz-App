from django.urls import path
from . import views

urlpatterns = [
    path('<int:quiz_id>', views.answerquiz, name='answerquiz'),
    path('match', views.quiz_match, name='quiz_match'),
]