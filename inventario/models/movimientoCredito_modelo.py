from django.db import models
from django.contrib.auth.models import User
from inventario.models.clienteCredito_modelo import ClienteCredito


class MovimientoCredito(models.Model):
    TIPO = [
        ('CARGO', 'Cargo (envío de mercancía)'),
        ('ABONO', 'Abono (pago recibido)'),
    ]

    cliente = models.ForeignKey(ClienteCredito, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPO)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    concepto = models.TextField(blank=True, help_text="Ej. 'Filtro aire.'")
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    cancelado = models.BooleanField(default=False)
    productos_json = models.JSONField(default=list, blank=True)
    
    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.tipo} - {self.cliente.nombre} - ${self.monto}"