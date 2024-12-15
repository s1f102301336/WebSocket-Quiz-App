from django.urls import path
from . import views

urlpatterns = [
    path('<int:quiz_id>', views.answerquiz, name='answerquiz'),
]