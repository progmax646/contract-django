from django.shortcuts import render, redirect, HttpResponse
from django.core.paginator import Paginator
from .forms import ContractForm, ContractBetaForm
from .models import Contract, Role
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from docxtpl import DocxTemplate
import datetime
import locale
from docx2pdf import convert
import pathlib
from bs4 import BeautifulSoup
import requests
from . import didox

# Create your views here.

# locale.setlocale(locale.LC_TIME, "ru.UTF-8")


def loginPage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            user_obj = Role.objects.get(user=user)
            if user_obj.title == 'account':
                return redirect('/contract/all-clients/'+str(user_obj.group))
            if user_obj.title == 'client':
                return redirect('/contract/get-user/'+str(user.id))
            if user_obj.id > 2:
                return redirect('/contract/all-client-full')
        else:
            messages.info(request, 'Username or Password incorrect')

    return render(request, 'contract/login.html')


@login_required(login_url='/login')
def contract_index(request, id):

    username = request.user

    # user = UserRole.objects.get(user=username)



    # получение captcha для инн
    captcha = []


    contracts = Contract.objects.filter(client_id = id)

    paginator = Paginator(contracts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    if request.method == 'POST':
        date = request.POST['date']
        day1 = str(date[8])
        day2 = str(date[9])
        day = day1+day2

        month1 = str(date[5])
        month2 = str(date[6])
        month = month1+month2

        result = day+'/'+month+'-1'
        try:
            contract_name = Contract.objects.filter(date=request.POST['date'], client_id=request.user.id)
            num = len(contract_name)
            if num != 0:
                result = day+'/'+month+'-'
                result += str(num+1)
        except Exception as e:
            pass

        # формирование договора в word
        try:

            # формирование даты в общепринятом формате
            date_inp = request.POST['date']
            date = datetime.date.fromisoformat(date_inp)
            company_name = Role.objects.get(user=request.user)
            print(company_name)
            doc = DocxTemplate(f"media/contracts/{company_name.company_name}/contract.docx")
            context = {'number': result, 'date':date.strftime("%d %B %Y")}
            doc.render(context)
            res = result.replace(result[2], '-')
            path = 'media/contracts/contract'+res+'.docx'
            doc.save(path)
            contract = Contract(comment=request.POST['comment'], date=request.POST['date'], contract_name=result,
                                path=path, client_id=request.user)
            contract.save()
        except Exception as e:
            print(e)


        return redirect('/contract/get-user/'+str(id))


    return render(request, "contract/index.html", {'form':ContractBetaForm, 'contracts':contracts, 'page_obj':page_obj,
                                                   'captcha':1, 'id':id, 'role':Role.objects.get(user=request.user), 'user_id':request.user.id})




def contract_status(request, id):

    contract = Contract.objects.get(id=id)
    contract.didox = 1
    contract.save()

    return redirect('/contract/get-user/'+str(contract.client_id.id))

def contract_status_del(request, id):

    contract = Contract.objects.get(id=id)
    contract.status = 2
    contract.save()

    return redirect('/contract/get-user/'+str(contract.client_id.id))


def contract_status_success(request, id):
    contract = Contract.objects.get(id=id)
    contract.status = 1
    contract.save()

    return redirect('/contract/get-user/'+str(contract.client_id.id))


def contract_search(request):
    if request.method == 'POST':
        name = request.POST['search']
        contracts = Contract.objects.filter(contract_name=name)
        return render(request, 'contract/search.html', {'contracts':contracts})


# редактирование контракта

def edit_contract(request, id):
    contract = Contract.objects.get(pk=id)
    company_name = Role.objects.get(user=request.user)

    date_inp = contract.date
    print(date_inp)
    date = datetime.date.fromisoformat(str(date_inp))
    result = contract.contract_name
    res = result.replace(result[2], '-')
    path = f'media/contracts/{company_name.company_name}/contract-edit' + res + '.docx'
    client = request.POST['client']
    director = request.POST['director']
    addres = request.POST['addres']
    client_inn = request.POST['client_inn']
    mfo = request.POST['mfo']
    check = request.POST['check']
    addres_bank = request.POST['addres_bank']
    oked = request.POST['oked']
    try:
        doc = DocxTemplate(f"media/contracts/{company_name.company_name}/contract_edit.docx")
        context = {'number': result, 'date': date.strftime("%d %B %Y"), 'client':client, 'director':director, 'addres':addres,
                   'client_inn': client_inn, 'mfo': mfo, 'check':check, 'addres_bank':addres_bank, 'oked': oked}
        doc.render(context)
        doc.save(path)
        return redirect('/contract/get-user/'+str(request.user.id))
    except Exception as e:
        print(e)


# форматирование word в pdf

def get_pdf(request, id):
    contract = Contract.objects.get(pk=id)
    company_name = Role.objects.get(user=request.user)
    result = contract.contract_name
    res = result.replace(result[2], '-')
    path_w = f'media/contracts/{company_name.company_name}/contract-edit'+res+'.docx'
    path_p = f'media/contracts/{company_name.company_name}/contract-edit'+res+'.pdf'
    file = pathlib.Path(path_w)
    if file.exists():
        try:
            convert(str(path_w))
            convert(str(path_w), str(path_p))
            convert(f"media/contracts{company_name.company_name}")
        except Exception as e:
            print(e)

        return redirect(f'/media/contracts/{company_name.company_name}/contract-edit'+res+'.pdf')
    else:
        path_w = f'media/contracts/{company_name.company_name}/contract-edit' + res + '.docx'
        path_p = f'media/contracts/{company_name.company_name}/contract-edit' + res + '.pdf'
        try:
            convert(str(path_w))
            convert(str(path_w), str(path_p))
            convert(f"media/contracts{company_name.company_name}")
        except Exception as e:
            print(e)

        return redirect(f'/media/contracts/{company_name.company_name}/contract-edit'+res+'.pdf')

def get_page(request, inn):

    headers = {'user-agent': 'my-app/0.0.1'}

    url = 'http://95.216.213.84:4567/hello/'+str(inn)

    get_info = requests.get(url, headers=headers)
    responce_info = get_info.json()

    client = responce_info['shortName']
    director = responce_info['director']
    address = responce_info['address']
    oked = responce_info['oked']
    account = responce_info['account']
    mfo = responce_info['mfo']


    return render(request, 'contract/form.html', {'client':client, 'director': director, 'addres': address, 'oked': oked,
                                                  'inn':inn, 'account':account, 'mfo':mfo})

def get_capcha(request):
    attr_url = []
    headers = {'user-agent': 'my-app/0.0.1'}
    statuz = requests.Session()
    cookies = {'PHPSESSID': 'lji24nfrp30ci8oklnc9dj0m06'}
    statuz = requests.get(url='http://registr.stat.uz/enter_form/ru/index.php', headers=headers, cookies=cookies)

    cookies_statuz = statuz.cookies
    capcha_stat = BeautifulSoup(statuz.content, 'html.parser')
    attr_url.clear()
    for i in capcha_stat.find_all('img'):
        attr_url.append(i['src'])

    url = attr_url[3]

    return render(request, 'contract/capcha.html', {'url':url})


# didox

def dodox_test(request):
    auth_id = ''
    # didox.getAuth('DS3045847270003')
    # didox.authDidox(auth_id, '65958562')
    return render(request, 'contract/test.html')


# create update delete user and client

def getUser(request):

    users = User.objects.all()

    if request.method == 'POST':

        name = request.POST['name']
        password = request.POST['password']
        email = request.POST['email']
        role_id = request.POST['role_id']
        group = request.POST['group']

        user = User.objects.create(name=name, password=password, email=email, role_id=role_id, group=group)
        user.save()

        return redirect('/contract/user')


    return render(request, 'contract/user/index.html', {'users':users})

def createUser(request):
    return render(request, 'contract/user/create.html')


def get_client_list(request, group):
    clients = Role.objects.filter(group=group, title='client')
    n = 0
    return render(request, 'contract/list_index.html', {'clients':clients, 'group':group, 'n':n})
    

def logout_user(request):
    logout(request)
    return redirect('/login')