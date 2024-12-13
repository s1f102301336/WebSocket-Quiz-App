from django.shortcuts import render

def login_view(request):
    return render(request, 'quiz/login.html')

def home_view(request):
    return render(request, 'quiz/home.html')

def answer_view(request):
    return render(request, 'quiz/answerquiz.html')

def makequiz_view(request):
    return render(request, 'quiz/makequiz.html')