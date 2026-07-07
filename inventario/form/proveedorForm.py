from django import forms
from inventario.models import ProveedorEmpresa

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = ProveedorEmpresa
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre", "id": "nombre"}
            ),
            "direccion": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Direccion",
                    "id": "direccion",
                }
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
            "sitio_web": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Sitio Web",
                    "id": "sitio_web",
                }
            ),
            "rfc": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "RFC", "id": "rfc"}
            ),
        }