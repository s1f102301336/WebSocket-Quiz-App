from django.shortcuts import render

# Create your views here.

def home_rooms(request):
    return render(request, 'home_rooms/home.html')