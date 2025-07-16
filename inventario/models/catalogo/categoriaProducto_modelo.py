from django.db import models
from catalogo.baseModel import BaseModel
from django.utils.translation import gettext_lazy as _



class CategoriaProducto(BaseModel):
    nombre = models.CharField(_("Nombre de categoría"), max_length=25, unique=True)
    descripcion = models.TextField(_("Descripción"), blank=True)
    padre = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategorias',
        verbose_name=_("Categoría padre")
    )

    class Meta:
        verbose_name = _("Categoría de producto")
        verbose_name_plural = _("Categorías de productos")
        ordering = ['nombre']

    def __str__(self):
        return self.nombre