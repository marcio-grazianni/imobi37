from pprint import pprint
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.contrib import auth

from django.http import HttpResponse



def inicio(request):
    return redirect('/accounts/login/')


def logar(request):
    # marcio - 1234
    # marcelo - 1234
    # fabiano - 1234

    retorno = ''
    print('Início')
    if request.method == "GET":
        print('Método GET')
        print(dir(request))
        print('-' * 60)
        print(dir(request.GET))
        print('-' * 60)
        print(dir(request.GET.items()))
        print('-' * 60)
        print(dir(request.user))
        print('-' * 60)
        print(request.user.is_authenticated)
        print('-' * 60)
        # retorno = request.GET.items()
    elif request.method == "POST":
        print('Método POST')
        # retorno = request.POST.items()
    # return HttpResponse(request.GET.items())

    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/plataforma')
        else:
            return render(request, 'logar.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        usuario = auth.authenticate(username=username, password=senha)

        if not usuario:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
            return redirect('/accounts/login')
        else:
            auth.login(request, usuario)
            return redirect(retorna_redirect_login(request, 'home'))


def retorna_redirect_login(request, pagina_padrao):
    """
    Verifica se tem na url a variavel 'next' e se ela não está vazia.
    params: request, pagina_padrao
    return: pagina_redirect
    """
    next = ""
    for header, value in request.META.items():
        if header == 'HTTP_REFERER':
            next = value
            break

    if "next" in next:
        next_lista = next.split("?")
        next_lista = next_lista[1].split("=")
        next = next_lista[1]
        return next
    else:
        return pagina_padrao


def cadastro(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'cadastro.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

    if len(username.strip()) == 0 or len(email.strip()) == 0 or len(senha.strip()) == 0:
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/cadastro/')

    user = User.objects.filter(username=username)

    if user.exists():
        messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse nome cadastrado')
        return redirect('/cadastro/')

    try:
        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=senha)
        user.save()
        messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso')
        return redirect('/accounts/login/')
    except:
        messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
        return redirect('/cadastro/')


@login_required
def sair(request):
    auth.logout(request)
    return redirect('/accounts/login')
