from django.db import models
from catalogo.baseModel import BaseModel
from django.utils.translation import gettext_lazy as _
from .provedorEmpresa_modelo import ProveedorEmpresa
from django.contrib.auth.models import User

class ContactoProveedor(BaseModel):
    TIPO_CONTACTO = [
        ('VENTAS', _('Ventas')),
        ('SOPORTE', _('Soporte técnico')),
        ('ADMIN', _('Administración')),
        ('OTRO', _('Otro')),
    ]

    proveedor = models.ForeignKey(
        ProveedorEmpresa,
        on_delete=models.CASCADE,
        related_name='contactos',
        verbose_name=_("Proveedor")
    )
    nombre = models.CharField(_("Nombre completo"), max_length=50)
    telefono = models.CharField(_("Teléfono"), max_length=15)
    email = models.EmailField(_("Correo electrónico"))
    tipo = models.CharField(
        _("Tipo de contacto"),
        max_length=10,
        choices=TIPO_CONTACTO,
        default='VENTAS'
    )
    puesto = models.CharField(_("Puesto"), max_length=50, blank=True)
    usuario=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='usuario',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("Contacto de proveedor")
        verbose_name_plural = _("Contactos de proveedores")
        ordering = ['proveedor', 'tipo', 'nombre']

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"