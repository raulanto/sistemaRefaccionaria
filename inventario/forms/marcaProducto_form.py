from django import forms
from inventario.models import marca_producto

class MarcaProductoForm(forms.ModelForm):
    class Meta:
        model = marca_producto
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }