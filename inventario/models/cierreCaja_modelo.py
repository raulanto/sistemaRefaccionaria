from django.db import models
from django.contrib.auth.models import User


class CierreCaja(models.Model):
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    total_ventas = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_ventas = models.PositiveIntegerField()
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Cierre {self.fecha_inicio.date()} — ${self.total_ventas}"