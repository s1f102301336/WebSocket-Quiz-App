from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('create_account/', views.create_accounts, name='create_account'),  # 関数名をそのまま
    path('logout/', views.logout_view, name='logout'),

]

