from django.db import models
from catalogo.baseModel import BaseModel
from django.utils.translation import gettext_lazy as _

from .catalogo.categoriaProducto_modelo import CategoriaProducto
from .contactoProvedor_modelo import ContactoProveedor
from .provedorEmpresa_modelo import ProveedorEmpresa
from django.core.validators import MinValueValidator
from .catalogo import Modelo,Marca,UnidadMedida


class Producto(BaseModel):
    ESTADO_PRODUCTO = [
        ('DISPONIBLE', _('Disponible')),
        ('AGOTADO', _('Agotado')),
        ('DESCONTINUADO', _('Descontinuado')),
        ('PEDIDO_ESPECIAL', _('Pedido especial')),
        ('Proximo a gotarse', _('proximo')),
    ]

    codigo = models.CharField(
        _("Código/Número de parte"),
        max_length=25,
        unique=True,
        help_text=_("Código único o número de parte del producto")
    )
    codigo_barras = models.CharField(
        _("Código de barras"),
        max_length=50,
        blank=True,
        null=True,
        unique=True
    )
    nombre = models.CharField(_("Nombre del producto"), max_length=100)
    descripcion = models.TextField(_("Descripción detallada"), blank=True)

    precio_compra = models.DecimalField(
        _("Precio de compra"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    precio_venta = models.DecimalField(
        _("Precio de venta al público"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    precio_mayoreo = models.DecimalField(
        _("Precio por mayoreo"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )
    cantidad_mayoreo = models.PositiveIntegerField(
        _("Cantidad mínima para mayoreo"),
        default=10,
        help_text=_("Cantidad mínima para aplicar precio por mayoreo")
    )

    stock = models.PositiveIntegerField(_("Existencia actual"), default=0)
    stock_minimo = models.PositiveIntegerField(
        _("Stock mínimo"),
        default=5,
        help_text=_("Cantidad mínima antes de generar alerta")
    )

    unidad_medida = models.ForeignKey(
        UnidadMedida,
        on_delete=models.PROTECT,
        related_name='productos',
        verbose_name=_("Unidad de medida")
    )

    modelo = models.ForeignKey(
        Modelo,
        on_delete=models.PROTECT,
        related_name='productos',
        verbose_name=_("Modelo"),
        help_text=_("Marca - modelo")
    )

    categoria = models.ForeignKey(
        CategoriaProducto,
        on_delete=models.PROTECT,
        related_name='productos',
        verbose_name=_("Categoría")
    )

    proveedor_principal = models.ForeignKey(
        ProveedorEmpresa,
        on_delete=models.PROTECT,
        related_name='productos',
        verbose_name=_("Proveedor principal")
    )

    contacto_proveedor = models.ForeignKey(
        ContactoProveedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='productos',
        verbose_name=_("Contacto para pedidos")
    )

    estado = models.CharField(
        _("Estado del producto"),
        max_length=30,
        choices=ESTADO_PRODUCTO,
        default='DISPONIBLE'
    )

    tiene_iva = models.BooleanField(_("Aplica IVA"), default=True)
    peso = models.DecimalField(
        _("Peso (kg)"),
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True
    )
    dimensiones = models.CharField(
        _("Dimensiones (LxAxH)"),
        max_length=50,
        blank=True,
        help_text=_("Ejemplo: 10x5x2 cm")
    )

    class Meta:
        verbose_name = _("Producto")
        verbose_name_plural = _("Productos")
        ordering = ['nombre']
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['codigo']),
            models.Index(fields=['codigo_barras']),
            models.Index(fields=['stock']),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    @property
    def necesita_reabastecimiento(self):
        return self.stock <= self.stock_minimo

    @property
    def margen_ganancia(self):
        if self.precio_compra == 0:
            return 0
        return ((self.precio_venta - self.precio_compra) / self.precio_compra) * 100


    def estado_producto(self):
        if self.stock <= 0:
            return 'AGOTADO'
        if self.stock < self.stock_minimo:
            return 'Proximo a gotarse'
        return 'DISPONIBLE'

    def save(self, *args, **kwargs):
        self.estado = self.estado_producto()
        super().save(*args, **kwargs)

