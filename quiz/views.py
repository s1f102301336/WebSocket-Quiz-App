from django.shortcuts import render
from django.http import Http404
from quiz_create.models import Quiz

# Create your views here.

def answerquiz(request, quiz_id):

    try:
        quiz = Quiz.objects.get(pk=quiz_id)
        
    except Quiz.DoesNotExist:
        raise Http404("Quiz does not exist")
    data={
        'quiz':quiz
    }
    return render(request, 'quiz/answerquiz.html', data)
