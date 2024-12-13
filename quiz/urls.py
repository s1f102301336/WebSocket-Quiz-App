from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.answerquiz, name='answerquiz'),
    # path('makequiz', views.makequiz, name='makequiz'),
    # path('login', views.login, name='login')
]