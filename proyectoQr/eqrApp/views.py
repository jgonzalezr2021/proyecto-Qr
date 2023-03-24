from django.shortcuts import redirect, render
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from eqrApp import models, forms
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required



def context_data():
    context = {
        'page_name' : '',
        'page_title' : 'Proyecto',
        'system_name' : 'Detector y generador de codigo QR y de barras',
        'topbar' : True,
        'footer' : True,
    }

    return context


# Create your views here.
def login_page(request):
    context = context_data()
    context['topbar'] = False
    context['footer'] = False
    context['page_name'] = 'login'
    context['page_title'] = 'Login'
    return render(request, 'login.html', context)

def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Nombre de usuario o contraseña incorrecto"
        else:
            resp['msg'] = "Nombre de usuario o contraseña incorrecto"
    return HttpResponse(json.dumps(resp),content_type='application/json')

@login_required
def home(request):
    context = context_data()
    context['page'] = 'home'
    context['page_title'] = 'Home'
    context['employees'] = models.Employee.objects.count()
    return render(request, 'home.html', context)

def logout_user(request):
    logout(request)
    return redirect('login-page')


@login_required
def employee_list(request):
    context =context_data()
    context['page'] = 'Listado Vcard'
    context['page_title'] = 'Listado de Vcard'
    context['employees'] = models.Employee.objects.all()

    return render(request, 'employee_list.html', context)

@login_required 
def manage_employee(request, pk=None):
    context =context_data()
    if pk is None:
        context['page'] = 'Añadir_Vcard'
        context['page_title'] = 'Añadir Vcard'
        context['employee'] = {}
    else:
        context['page'] = 'Editar_vcard'
        context['page_title'] = 'Actualizar Vcard'
        context['employee'] = models.Employee.objects.get(id=pk)

    return render(request, 'manage_employee.html', context)

@login_required
def save_employee(request):
    resp = { 'status' : 'failed', 'msg' : '' }
    if not request.method == 'POST':
        resp['msg'] = "No se han enviado datos a la solicitud."

    else:
        if request.POST['id'] == '':
            form = forms.SaveEmployee(request.POST, request.FILES)
        else:
            employee = models.Employee.objects.get(id = request.POST['id'])
            form = forms.SaveEmployee(request.POST, request.FILES, instance = employee)
        if form.is_valid():
            form.save()
            if request.POST['id'] == '':
                messages.success(request, f"{request.POST['codigo_empleado']} se ha añadido con éxito.")
            else:
                messages.success(request, f"{request.POST['codigo_empleado']} se ha actualizado correctamente.")
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    if not resp['msg'] == '':
                        resp['msg'] += str("<br />")
                    resp['msg'] += str(f"[{field.label}] {error}")

    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def view_card(request, pk =None):
    if pk is None:
        return HttpResponse("El id de la Vcard es invalido")
    else:
        context = context_data()
        context['employee'] = models.Employee.objects.get(id=pk)
        return render(request, 'view_id.html', context)

@login_required
def view_scanner(request):
    context = context_data()
    return render(request, 'scanner.html', context)


@login_required
def view_details(request, code = None):
    if code is None:
        return HttpResponse("El código de Vcard no es válido")
    else:
        context = context_data()
        context['employee'] = models.Employee.objects.get(codigo_empleado =code)
        return render(request, 'view_details.html', context)

@login_required
def delete_employee(request, pk=None):
    resp = { 'status' : 'failed', 'msg' : '' }
    if pk is None:
        resp['msg'] = "No se han enviado datos a la solicitud."
    else:
        try:
            models.Employee.objects.get(id=pk).delete()
            resp['status'] = 'success'
            messages.success(request, 'La Vcard ha sido eliminada con éxito.')
        except:
            resp['msg'] = "La Vcard no se pudo eliminar."

    return HttpResponse(json.dumps(resp), content_type="application/json")
