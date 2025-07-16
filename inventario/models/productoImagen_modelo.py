from django.db import models
from catalogo.baseModel import BaseModel
from django.utils.translation import gettext_lazy as _


from .producto_modelo import Producto



class ProductoImagen(BaseModel):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='imagenes'
    )
    imagen = models.ImageField(
        _("Imagen del producto"),
        upload_to='productos/'
    )
    orden = models.PositiveSmallIntegerField(_("Orden de visualización"), default=0)
    es_principal = models.BooleanField(_("Imagen principal"), default=False)

    class Meta:
        verbose_name = _("Imagen de producto")
        verbose_name_plural = _("Imágenes de productos")
        ordering = ['producto', 'orden']
        unique_together = ['producto', 'orden']

    def __str__(self):
        return f"Imagen {self.orden} de {self.producto}"