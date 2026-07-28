from django import forms
from inventario.models.catalogo.marca_producto import MarcaProducto

class MarcaProductoForm(forms.ModelForm):
    class Meta:
        model = MarcaProducto
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }