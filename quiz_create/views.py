from django.shortcuts import render

# Create your views here.

def quiz_create(request):
    return render(request, 'quiz_create/makequiz.html')