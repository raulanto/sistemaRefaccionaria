from django.db import models
from simple_history.models import HistoricalRecords

class BaseModel(models.Model):
    """
    Clase base para todos los modelos de la aplicación.
    Contiene campos comunes y métodos útiles.
    """
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    historia = HistoricalRecords(inherit=True)
    activo = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def toggle_activo(self):
        self.activo = not self.activo
        self.save()