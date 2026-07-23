from django import forms
from inventario.models import Producto


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = "__all__"
        widgets = {
            "codigo": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Codigo", "id": "codigo"}
            ),
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre", "id": "nombre"}
            ),
            "descripcion": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descipcion",
                    "id": "descripcion",
                }
            ),
            "precio_compra": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "$0.00"}
            ),
            "precio_venta": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "$0.00"}
            ),
            "precio_mayoreo": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "$0.00"}
            ),
            "cantidad_mayoreo": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "$0.00"}
            ),
            "stock": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Estock actual",
                    "id": "stock",
                }
            ),
            "stock_minimo": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Estock Minimo",
                    "id": "sotck_minimo",
                }
            ),
            "unidad_medida": forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Unidad de Medida",
                    "id": "unidad_medida",
                }
            ),
            "categoria": forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Categoria",
                    "id": "categoria",
                }
            ),
            "marca": forms.Select(
                attrs={
                    "class": "form-select shadow-sm",
                    "placeholder": "marca",
                    "id": "marca",
                }
            ),
            "proveedor_principal": forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Proveedor Principal",
                    "id": "proveedor_principal",
                }
            ),
            "contacto_proveedor": forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Contacto para pedidos",
                    "id": "contacto_proveedor",
                }
            ),
            "estado": forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Estado del Producto",
                    "id": "estado",
                }
            ),
        }
