from django.shortcuts import render, redirect
from .models import Quiz
from .forms import QuizForm


# Create your views here.
#未入力の場合alert発生させる
#作成したらページも作成
#自分が作成したクイズのみ、編集や削除ができると良い

def quiz_create(request):
    return render(request, 'quiz_create/makequiz.html')

def makequiz(request):
    data = {}
    print(request)
    print(request.POST)
    if request.method == 'POST':
        form = QuizForm(request.POST)#requestの内容をFormに送り、Formが自動的にmodel化する
        if form.is_valid():#modelに設定した制限に当てはまるか検証
            post = form.save(commit=False)
            post.save()
            print(post.pk)
            return redirect('/', quiz_id=post.pk)#home.htmlへ
        else:
            print(form.errors)#必須ですとconsole表示、リダイレクト
    else:
        form = QuizForm()

    return render(request, "quiz_create/makequiz.html",{'form':form}) #POSTでないタブの更新や、form.is_valid()がFalseの時の操作
#未入力エラーをHTMLに記載したいときは {'form':form})を使いそう