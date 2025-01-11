from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def login(request):
    if request.method == 'POST':
        username = request.POST.get('user-id')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'ユーザIDまたはパスワードが間違っています')
    return render(request, 'accounts/login.html')

def create_accounts(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'パスワードが一致しません。')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'このユーザIDは既に使用されています。')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'アカウントが作成されました！ログインしてください。')
            return redirect('login')

    return render(request, 'accounts/create_account.html')



def logout_view(request):
    logout(request)
    return redirect('home')