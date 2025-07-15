
from django.db import models
from catalogo.baseModel import BaseModel
from django.utils.translation import gettext_lazy as _
from .marca_modelo import Marca


class Modelo(BaseModel):
    nombre = models.CharField(_("Nombre de Modelo"), max_length=35, unique=True)
    marca = models.ForeignKey(
        Marca,
        on_delete=models.CASCADE,
        related_name='modelos',
        verbose_name=_("Marca asociada")
    )

    class Meta:
        verbose_name = _("Modelo")
        verbose_name_plural = _("Modelos")
        ordering = ['marca', 'nombre']
        unique_together = ['nombre', 'marca']

    def __str__(self):
        return f"{self.marca} - {self.nombre}"