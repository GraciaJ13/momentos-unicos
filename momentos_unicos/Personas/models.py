from django.db import models

# Create your models here. Son como las tablas en la base de datos
class Persona(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, unique=True)
    cedula = models.IntegerField(null=True)
    username = models.CharField(max_length=50, null= True, unique=True)
    password_hash = models.CharField(max_length=255, null=True)
    
class Boda(models.Model):
    nombre_boda = models.CharField(max_length=50, null=False)
    fecha_boda = models.DateField(null=False) 
    lugar = models.CharField(max_length=200) 
    codigo_boda = models.CharField(max_length=50, unique=True, null=False)
    
    
class Regalo(models.Model):
      
    nombre= models.CharField(max_length=100)
    descripcion= models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=5)
    url= models.CharField(max_length=100)
    nombre= models.CharField(max_length=50, default='disponible')   
    
    
class Invitado(models.Model):
    nombre = models.CharField(max_length=100, null=False)  
    email = models.EmailField(max_length=150, null=True)
    telefono = models.CharField(max_length=20, null=True)
    boda = models.ForeignKey(Boda, on_delete=models.CASCADE)
    invitado_registrado_por = models.ForeignKey(Persona, on_delete=models.SET_NULL, null=True)
    regalo = models.ForeignKey(Regalo, on_delete=models.SET_NULL, null=True, blank=True)