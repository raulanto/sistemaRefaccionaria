from django.db import models
from catalogo.baseModel import BaseModel
from django.utils.translation import gettext_lazy as _

class Marca(BaseModel):
    nombre = models.CharField(_("Nombre de Marca"), max_length=35, unique=True)

    class Meta:
        verbose_name = _("Marca")
        verbose_name_plural = _("Marcas")
        ordering = ['nombre']

    def __str__(self):
        return self.nombre