from django.shortcuts import render, redirect
from.models import Producto
from django.contrib import messages
from django.http.response import JsonResponse
from django.views.generic import View

# Create your views here.


def lista(request):
    productosListados = Producto.objects.all()
    
    return render(request, "gestionProductos.html", {"productos": productosListados})
def post(self,request,*args,**kwargs):
    if request.method=="POST":
        producto_ids=request.POST.getlist('id[]')
        for codigo in producto_ids:
            product=  Producto.objects.get(codigo=codigo)
            product.delete()
        return redirect('gestionProductos')

def registarProducto(request):
    codigo = request.POST['txtCodigo']
    nombre = request.POST['txtNombre']
    valor = request.POST['numValor']

    producto = Producto.objects.create(codigo=codigo, nombre=nombre, valor=valor)
    messages.success(request, '¡Registro registrado!')
    return redirect('gestionProductos')


def edicionProducto(request, codigo):
    producto = Producto.objects.get(codigo=codigo)
    return render(request, "edicionProducto.html", {"producto": producto})   

def editarProducto(request):
    codigo = request.POST['txtCodigo']
    nombre = request.POST['txtNombre']
    valor = request.POST['numValor']

    
    producto = Producto.objects.get(codigo=codigo)

    producto.nombre = nombre
    producto.valor = valor
    producto.save()

    messages.success(request, '¡Registro actualizado!')

    return redirect('gestionProductos')

def eliminarProducto(request, codigo):
    producto = Producto.objects.get(codigo=codigo)
    producto.delete()

    messages.success(request, '¡Registro eliminado!')

    return redirect('gestionProductos')

def check_mychecklist(request):
           
    if request.method== 'POST':

        for i in Producto.objects.filter(status=1):
         print(i.pk)
        x=request.POST.get(str(i.pk))
        print(x)
        if str(x) == 'on':
            b=Producto.objects.get(pk=i.pk)
            b.delete()
    return redirect('gestionProductos')

def list_productos(_request):
    productos = list(productos.objects.values())
    data = {'productos': productos}
    return JsonResponse(data)