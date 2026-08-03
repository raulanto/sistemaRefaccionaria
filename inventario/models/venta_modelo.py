from django.db import models
from django.contrib.auth.models import User


class Venta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    cierre = models.ForeignKey('CierreCaja', on_delete=models.SET_NULL, null=True, blank=True, related_name='ventas')
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # 👈 nuevo

    estado = models.CharField(
            max_length=20,
            default="activa"
        )
    
    def __str__(self):
        return f"Venta {self.id}"
    
    
    # en models/venta.py
