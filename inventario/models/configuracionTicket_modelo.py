from django.db import models

class ConfiguracionTicket(models.Model):
    nombre_empresa = models.CharField(max_length=100)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    correo = models.EmailField(max_length=100, null=True)
    direccion = models.TextField(blank=True, null=True)
    
    mensaje_final = models.CharField(
        max_length=255,
        default = "Gracias por su compra, vuelva pronto.",
    )
    
    def __str__(self):
        return self.nombre_empresa