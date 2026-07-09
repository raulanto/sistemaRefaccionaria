from django import forms
from inventario.models import ContactoProveedor

class ContactoProveedorForm(forms.ModelForm):
    class Meta:
        model = ContactoProveedor
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre", "id": "nombre"}
            ),
            "proveedor": forms.Select(
                attrs={"class": "form-control", "placeholder": "Proveedor", "id": "proveedor"}
            ),
            "telefono": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Telefono",
                    "id": "telefono",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Correo Electronico",
                    "id": "correo_electronico",
                }
            ),
            "tipo": forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Tipo de contacto",
                    "id": "tipo",
                }
            ),
        }