from secrets import choice
from django import forms
from numpy import require
from eqrApp import models
import qrcode

class SaveEmployee(forms.ModelForm):
    codigo_empleado = forms.CharField(max_length=250, label="codigo de empleado")
    primer_nombre = forms.CharField(max_length=250, label="primer nombre")
    segundo_nombre = forms.CharField(max_length=250, label="segundo nombre", required=False)
    apellido = forms.CharField(max_length=250, label="apellido")
    dob = forms.DateField(label="Birthday")
    genero = forms.ChoiceField(choices=[("masculino","masculino"), ("femenino","femenino")], label="Genero")
    contacto = forms.CharField(max_length=250, label="Contacto #")
    email = forms.CharField(max_length=250, label="Email")
    direccion = forms.Textarea()
    departamento = forms.CharField(max_length=250, label="Departamento")
    posicion = forms.CharField(max_length=250, label="Posicion")
    avatar = forms.ImageField(label="Avatar")

    class Meta():
        model = models.Employee
        fields = ('codigo_empleado',
                  'primer_nombre',
                  'segundo_nombre',
                  'apellido',
                  'dob',
                  'genero',
                  'contacto',
                  'email',
                  'direccion',
                  'departamento',
                  'posicion',
                  'avatar', )

    def clean_employee_code(self):
        id = self.data['id'] if self.data['id'] != '' else 0
        codigo_empleado = self.cleaned_data['codigo_empleado']
        try:
            if id > 0:
                employee = models.Employee.exclude(id=id).get(codigo_empleado= codigo_empleado)
            else:
                employee = models.Employee.get(codigo_empleado = codigo_empleado)
        except:
            return codigo_empleado
        return forms.ValidationError(f"{codigo_empleado} ya existe.")

