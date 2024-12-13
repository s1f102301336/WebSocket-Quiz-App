from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'quiz/home.html')

def answerquiz(request):
    return render(request, 'quiz/answerquiz.html')

def makequiz(request):
    return render(request, 'quiz/makequiz.html')

def login(request):
    return render(request, 'quiz/login.html')