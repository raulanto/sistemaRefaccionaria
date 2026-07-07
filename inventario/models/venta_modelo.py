from django.db import models

class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta {self.id}"
    
    estado = models.CharField(
        max_length=20,
        default="activa"
    )