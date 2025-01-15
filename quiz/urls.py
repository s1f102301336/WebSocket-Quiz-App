from django.urls import path
from . import views

urlpatterns = [
    path('<int:quiz_id>', views.answerquiz, name='answerquiz'),
    path('match/<str:category>/', views.quiz_match, name='quiz_match'),  # match/<category>を定義
    path('get_data/<str:category>/', views.get_data, name='get_data'),  # get_data/<category>を定義
]
