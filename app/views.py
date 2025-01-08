from curses.ascii import isspace
import json
from django.core.paginator import Paginator
from tabnanny import check
from urllib import response
from validate_docbr import CPF,CNPJ
from django.contrib import auth, messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
import requests
import re
from django.contrib.auth.decorators import login_required
from email_validator import validate_email, EmailNotValidError
from app.models import Tipo, Verif

# Create your views here.

def handler404(request, exception):
    return render(request,'not-found.html')

def cadastro(request):
    if request.method == 'POST':
        resp = request.POST.get('resposta')

        if resp == 'empresa':
            return redirect('infos_empresa')
        else:
            return redirect('infos_anunciante')
    else:
        return render(request,'quest.html')


def logar(request):
    if request.method == 'POST':

        usuario = request.POST.get('usuario')
        senha =request.POST.get('senha')
        email = request.POST.get('email')

        check = auth.authenticate(request, username=usuario, password=senha)

        if check is None:
            messages.info(request,'o usuario ou senha inválidos')
            return redirect('login')
        else:
            login(request,check)
            return redirect('main')
    else:
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('main')


def infos_empresa(request):
    if request.method == 'POST':
        
        cnpj = request.POST.get('cnpj')

        #validação CPNJ
        
        cnpj_validate = CNPJ()

        if cnpj_validate.validate(f'{cnpj}') == False:
            messages.info(request,'CNPJ inválido')
            return redirect('infos_empresa')

        cnpj_post = cnpj_validate.mask(cnpj)

        senha = request.POST.get('senha')
        repeat_senha = request.POST.get('r_senha')

        response = requests.get(f'https://receitaws.com.br/v1/cnpj/{cnpj}/').json()

        usuario = response["nome"]
        em = response["email"]

        users = User.objects.all()

        for x in users:
            if x.username == usuario:
                messages.info(request,'usuario já existente')
                return redirect('infos_empresa')

            if senha != repeat_senha:
                messages.info(request,'as senhas informadas são diferentes')
                return redirect('infos_empresa')


        user = User.objects.create_user(username=usuario, password=senha)
        user.save()

        requests.post('http://127.0.0.1:8000/infempresas/', json = {
            "nome": f"{response['nome']}",
            "cnpj": f"{cnpj_post}",
            "rua": f"{response['logradouro']}",
            "bairro": f"{response['bairro']}",
            "cidade": f"{response['municipio']}",
            "numero": f"{response['telefone']}",
            "email": f"{response['email']}"
        })

        return redirect('main')
    else:
        return render(request, 'cadastroEmpresa.html')

def infos_anunciante(request):


    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        repeat_senha = request.POST.get('repeat_senha')

        if usuario.isspace() == True or cpf.isspace() == True or email.isspace() == True or senha.isspace() == True or repeat_senha.isspace() == True:
            messages.info(request, 'os campos não podem estar em branco')
            return redirect('infos_anunciante')


        #validação do cpf

        


        valid = CPF()
        
        if valid.validate(f'{cpf}') == False:
            messages.info(request, 'cpf inválido')
            return redirect('infos_anunciante')

        cpf_post = valid.mask(cpf)


        verif = Verif.objects.all()
        for x in verif:
            if x.cpf_cnpj == cpf:
                messages.info(request,'o cpf ja foi cadastrado')
                return redirect('infos_anunciante')

        #validação do email
        
        try:
            email_validate = validate_email(email).email
        except EmailNotValidError as e:
            messages.info(request,'E-mail inválido')
            return redirect('infos_anunciante')


        users = User.objects.all()

        for x in users:
            if x.username == usuario:
                messages.info(request,'usuario já existente')
                return redirect('infos_anunciante')

            if senha != repeat_senha:
                messages.info(request,'as senhas informadas são diferentes')
                return redirect('infos_anunciante')


        verificacao = Verif.objects.create(cpf_cnpj=cpf)
        verificacao.save()

        user = User.objects.create_user(username=usuario, password=senha)
        user.save()

        tipo = Tipo.objects.create(nome=usuario,tipo='anunciante')
        tipo.save()

        requests.post(url = 'http://127.0.0.1:8000/infanunciante/', json = {
            "nome": f"{usuario}",
            "cpf": f"{cpf_post}",
            "email": f"{email}"
        })
        
        return redirect('main')
    else:
        return render(request,'cadastroAnun.html')


@login_required(redirect_field_name='login/') 
def anunciar(request):
    if request.method == 'POST':
    
        lograd = request.POST.get('logradouro')
        numero = request.POST.get('numero')
        nomerua = request.POST.get('rua')
        bairro = request.POST.get('bairro')
        security = request.POST.get('seguranca')
        tipo = request.POST.get('tipo')
        desc = request.POST.get('desc')
        print(desc,tipo)

        print(security)

        if lograd.isspace() == 'True' or nomerua.isspace() == 'True' or bairro.isspace() == 'True' or tipo.isspace() == 'True' or desc.isspace() == 'True' or security.isspace() == 'True':
            messages.info(request, 'os campos não podem estar em branco')
            return redirect('anunciar')

        #validação do número de telefone

        if len(numero) != 11:
            messages.info(request,'número inválido')
            return redirect('anunciar')

        padrao = "([0-9]{2,3})?([0-9]{2})([0-9]{4,5})([0-9]{4})"

        resposta = re.search(padrao, numero)
        numb = ('+55({}){}-{}'.format(numero[0:2], numero[2:7], numero[7:11]))    
        print(numb)
        print(type(tipo))
        
        requests.post(url = 'http://127.0.0.1:8000/anuncio/', json = {
            "usuario":f"{request.user.username}",
            "numero": f"{numb}",
            "logradouro":f"{lograd}",
            "nome_da_rua":f"{nomerua}",
            "bairro": f"{bairro}",
            "tipo": f"{tipo}",
            "desc": f"{desc}",
            "seg": f"{security}"
        })
        
        return redirect('main')
    else:
        return render(request, 'anunciar.html')


@login_required(redirect_field_name='login/') 
def meus_anuncios(request):

    tip = Tipo.objects.all()

    check=''

    for i in tip:
        if i.nome == request.user:
            check += 'True'
            break

    response = requests.get(url = 'http://127.0.0.1:8000/anuncio/').json()

    sla = json.dumps(response)
    sl = json.loads(sla)

    return render(request, 'meus_anuncios.html',{'response':response,'check':check,'sl':sl})


@login_required(redirect_field_name='login/') 
def remover_anuncio(request,id):

    requests.delete(url = f'http://127.0.0.1:8000/anuncio/{id}/')

    return redirect('meus_anuncios')


def main(request):
    response = requests.get('http://127.0.0.1:8000/anuncio/').json()
    
    tip = Tipo.objects.all()

    check=''

    for i in tip:
        if i.nome == request.user.username:
            check += 'True'
            break

    return render(request,'main.html',{'response':response,'check':check})

def sobre(request):

    tip = Tipo.objects.all()

    check=''

    for i in tip:
        if i.nome == request.user.username:
            check += 'True'
            break

    return render(request,'sobre.html',{'check':check})

def plastico(request):
    response = requests.get(f'http://127.0.0.1:8000/anuncio/?search=Plastico').json()

    tip = Tipo.objects.all()

    check=''

    for i in tip:
        if i.nome == request.user.username:
            check += 'True'
            break


    return render(request,'main.html', {'response':response,'check':check})

def vidro(request):
    response = requests.get(f'http://127.0.0.1:8000/anuncio/?search=Vidro').json()

    tip = Tipo.objects.all()

    check=''

    for i in tip:
        if i.nome == request.user.username:
            check += 'True'
            break

    return render(request,'main.html', {'response':response,'check':check})

def papel(request):
    response = requests.get(f'http://127.0.0.1:8000/anuncio/?search=papel').json()

    tip = Tipo.objects.all()

    check=''

    for i in tip:
        if i.nome == request.user.username:
            check += 'True'
            break

    return render(request,'main.html', {'response':response,'check':check})


def metal(request):
    response = requests.get(f'http://127.0.0.1:8000/anuncio/?search=metal').json()

    tip = Tipo.objects.all()

    check=''

    for i in tip:
        if i.nome == request.user.username:
            check += 'True'
            break

    return render(request,'main.html', {'response':response,'check':check})


def organico(request):
    response = requests.get(f'http://127.0.0.1:8000/anuncio/?search=organico').json()

    tip = Tipo.objects.all()

    check=''

    for i in tip:
        if i.nome == request.user.username:
            check += 'True'
            break

    return render(request,'main.html', {'response':response,'check':check})



