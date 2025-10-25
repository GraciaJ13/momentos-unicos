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
    usuario = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True, blank=True)  # Nuevo campo

    def __str__(self):
        return self.nombre_boda
    
    
class Regalo(models.Model):
      
    nombre= models.CharField(max_length=100)
    descripcion= models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=5)
    url= models.CharField(max_length=100)
    estado= models.CharField(max_length=50, default='disponible')   
    boda_id = models.ForeignKey(Boda, on_delete=models.CASCADE, null=False)
    
class Invitado(models.Model):
    nombre = models.CharField(max_length=100, null=False)  
    email = models.EmailField(max_length=150, null=True)
    telefono = models.CharField(max_length=20, null=True)
    boda = models.ForeignKey(Boda, on_delete=models.CASCADE)
    invitado_registrado_por = models.ForeignKey(Persona, on_delete=models.SET_NULL, null=True)
    regalo = models.ForeignKey(Regalo, on_delete=models.SET_NULL, null=True, blank=True)
    
class Reserva_regalo(models.Model):
    invitado = models.ForeignKey(Invitado, on_delete=models.CASCADE)
    regalo = models.ForeignKey(Regalo, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, default='reservado')  # Ejemplo de estado

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    servicio = models.CharField(max_length=200, null=False)
    contacto = models.CharField(max_length=100, null=False)
    telefono = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=150, null=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
class Servicio_proveedor(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    boda = models.ForeignKey(Boda, on_delete=models.CASCADE)
    
class Contratacion_servicio(models.Model):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio_proveedor, on_delete=models.CASCADE)
    fecha_contratacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, default='pendiente')  # Ejemplo de estado
    
class Cancion(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    artista = models.CharField(max_length=100, null=False)
    invitado = models.ForeignKey(Invitado, on_delete=models.CASCADE, unique=True)  # Una sola canción por invitado
    boda = models.ForeignKey(Boda, on_delete=models.CASCADE)
    fecha_agregada = models.DateTimeField(auto_now_add=True)