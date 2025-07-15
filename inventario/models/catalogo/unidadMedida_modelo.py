
from django.db import models
from catalogo.baseModel import BaseModel
from django.utils.translation import gettext_lazy as _



class UnidadMedida(BaseModel):
    nombre = models.CharField(_("Nombre"), max_length=20, unique=True)
    abreviatura = models.CharField(_("Abreviatura"), max_length=5, unique=True)

    class Meta:
        verbose_name = _("Unidad de medida")
        verbose_name_plural = _("Unidades de medida")
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.abreviatura})"