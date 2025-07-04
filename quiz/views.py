from django.shortcuts import render
from django.http import Http404
from quiz_create.models import Quiz
from django.db.models import Q
from django.http import Http404, JsonResponse
import random



# Create your views here.

def answerquiz(request, quiz_id):

    try:
        quiz = Quiz.objects.filter(pk=quiz_id).values(
             'id', 'title', 'content', 'category', 'description', 'explanation'
        ).first()
        q = Quiz.objects.filter(pk=quiz_id).values(
             'correct_answer', 'incorrect1', 'incorrect2', 'incorrect3'
        )
        s = list(q)[0]
        selections = {
            'correct_answer':s['correct_answer'],
            'incorrect1':s['incorrect1'],
            'incorrect2':s['incorrect2'],
            'incorrect3':s['incorrect3']
            }
        items = list(selections.items())
        random.shuffle(items)

        shuffled_selections = dict(items)
        print("shuffled_selections", shuffled_selections)
        print("quiz", quiz)
        
    except Quiz.DoesNotExist:
        raise Http404("Quiz does not exist")
    
    return render(request, 'quiz/answerquiz.html', {"quiz":quiz, "selections":shuffled_selections})

def quiz_match(request, category):
    print("category", category)
    return render(request, 'quiz/quiz_match.html',{"category":category})

def get_data(request, category):

    if (category=="ALL"):
            quizzes = Quiz.objects.all().order_by('-id')

    else:
    # 完全一致でクエリをフィルタリング
        quizzes = Quiz.objects.filter(category=category).order_by('-id')
    
    # デバッグ用の出力
    print(f"Category from URL: {category}")  # URLから受け取ったカテゴリ
    print(f"Retrieved quizzes: {quizzes}")  # 取得したクイズ

    # データが存在しない場合のハンドリング
    if not quizzes.exists():
        return JsonResponse({"error": "No quizzes found for this category", "title":"該当するクイズがありません。"}, status=404)
    
    # クエリセットをJSONレスポンスで返す
    return JsonResponse(list(quizzes.values(), ), safe=False)
