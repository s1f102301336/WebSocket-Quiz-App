from django.shortcuts import render
from quiz_create.models import Quiz

# Create your views here.

def home_rooms(request):
    data = {
        "quiz_result" : Quiz.objects.all()
    }
    # print(data)
    # print("これがデータです",data["quiz_result"].query)
    return render(request, 'home_rooms/home.html', data)