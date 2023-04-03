from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
import qrcode
from PIL import Image

# Create your models here.
class Employee(models.Model):
    codigo_empleado = models.CharField(max_length=100)
    primer_nombre = models.CharField(max_length=250)
    segundo_nombre = models.CharField(max_length=250, null=True)
    apellido = models.CharField(max_length=250)
    genero = models.CharField(max_length=50, choices=(("masculino","masculino"), ("femenino","femenino")), default="masculino")
    dob = models.DateField(max)
    contacto = models.CharField(max_length=100)
    email = models.CharField(max_length=250, blank=True)
    direccion = models.TextField(null=True, blank=True)
    departamento  = models.TextField(null=True, blank=True)
    posicion = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to = "avatars/",null=True, blank=True)
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(f"{self.codigo_empleado} - {self.primer_nombre} "+ (f"{self.segundo_nombre} {self.apellido}" if not self.segundo_nombre == "" else f"{self.apellido}") )
    def name(self):
        return str(f"{self.primer_nombre} "+ (f"{self.segundo_nombre} {self.apellido}" if not self.segundo_nombre == "" else f"{self.apellido}") )


    def save(self, *args, **kwargs):
        super(Employee, self).save(*args, **kwargs)
        print(self.avatar)
        imag = Image.open(self.avatar.path)
        if imag.width > 200 or imag.height> 200:
            output_size = (200, 200)
            imag.thumbnail(output_size)
            imag.save(self.avatar.path)
        
