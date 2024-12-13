from django.urls import path
from . import views

urlpatterns = [
	path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('answerquiz/', views.answer_view, name='answerquiz'),
    path('makequiz/',views.makequiz_view,name = 'makequiz'),
    
]