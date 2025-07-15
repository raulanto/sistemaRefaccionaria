from django.db import models
from catalogo.baseModel import BaseModel
from django.utils.translation import gettext_lazy as _



class ProveedorEmpresa(BaseModel):
    nombre = models.CharField(_("Nombre de la empresa"), max_length=50, unique=True)
    telefono = models.CharField(_("Teléfono"), max_length=15)
    email = models.EmailField(_("Correo electrónico"))
    direccion = models.TextField(_("Dirección"), blank=True)
    rfc = models.CharField(_("RFC"), max_length=13, blank=True, null=True)
    sitio_web = models.URLField(_("Sitio web"), blank=True)

    class Meta:
        verbose_name = _("Proveedor")
        verbose_name_plural = _("Proveedores")
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
