from django.db import models
from django.contrib.auth.models import User
from .producto_modelo import Producto


class MovimientoInventario(models.Model):
    TIPO_MOVIMIENTO = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
    ]
    MOTIVOS = [
        ('COMPRA', 'Compra a proveedor'),
        ('DEVOLUCION_CLIENTE', 'Devolución de cliente'),
        ('DEVOLUCION_PROVEEDOR', 'Devolución a proveedor'),
        ('MERMA', 'Merma / Daño'),
        ('AJUSTE', 'Ajuste de inventario'),
        ('OTRO', 'Otro'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO)
    cantidad = models.PositiveIntegerField()
    motivo = models.CharField(max_length=30, choices=MOTIVOS, default='OTRO')
    observaciones = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"