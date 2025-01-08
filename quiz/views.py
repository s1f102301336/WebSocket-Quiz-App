from django.shortcuts import render
from django.http import Http404
from quiz_create.models import Quiz
from django.db.models import Q
from django.http import Http404, JsonResponse



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

def quiz_match(request, category):
    return render(request, 'quiz/answerquiz.html',{"category":category})

def get_data(request, category):
    quizzes = Quiz.objects.order_by('-id')#ランダムにしよう
    selected_category = category
    if selected_category:  # 選択された場合にフィルタリング
        quizzes = quizzes.filter(
            Q(category__icontains=selected_category))
    else:  # "ALL" を選択した場合
        print("ALL")
        quizzes = Quiz.objects.all()
        print(quizzes)
    return JsonResponse(list(quizzes), safe=False)