from django.urls import path
from . import views

urlpatterns = [
    path('<int:quiz_id>', views.answerquiz, name='answerquiz'),
    path('match/<str:category>', views.quiz_match, name='quiz_match'),
    path('get_data', views.get_data, name="get_data"),
]