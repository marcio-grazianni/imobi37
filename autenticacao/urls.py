from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('accounts/login/', views.logar, name='logar'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('sair/', views.sair, name='sair'),
]
