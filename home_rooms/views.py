from django.shortcuts import render
from quiz_create.models import Quiz
from django.db.models import Q

# Create your views here.

def home_rooms(request):
    quizzes = Quiz.objects.order_by('-id')
    selected_category = request.GET.get('category', '')  # デフォルトは空文字
    print(selected_category)
    if selected_category:  # 選択された場合にフィルタリング
        quizzes = quizzes.filter(
            Q(category__icontains=selected_category))
    else:  # "ALL" を選択した場合
        print("ALL")
        quizzes = Quiz.objects.all()
    return render(request, 'home_rooms/home.html', {'quizzes':quizzes,'selected_category':selected_category})