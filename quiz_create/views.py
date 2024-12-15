from django.shortcuts import render
from .models import Quiz

# Create your views here.

def quiz_create(request):
    return render(request, 'quiz_create/makequiz.html')

def makequiz(request):
    data = {}
    print(request)
    print(request.POST)
    if request.method == 'POST':
        category = (request.POST["category"]).upper()
        title = request.POST["title"]
        content = request.POST["content"]
        correct_answer = request.POST["correct_answer"]
        incorrect1 = request.POST["incorrect1"]
        incorrect2 = request.POST["incorrect2"]
        incorrect3 = request.POST["incorrect3"]
        explanation = request.POST["explanation"]
        result = Quiz(
            category = category, 
            title = title, 
            content = content, 
            correct_answer = correct_answer, 
            incorrect1 = incorrect1, 
            incorrect2 = incorrect2, 
            incorrect3 = incorrect3, 
            explanation = explanation)
        result.save()
    
    quiz_result = Quiz.objects.all()
    data["quiz_result"] = quiz_result
    return render(request, "quiz_create/makequiz.html", data)