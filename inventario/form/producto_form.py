from django.forms import ModelForm
from django import forms
from inventario.models import Producto

class ProductoForm(ModelForm):

    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'nombre':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Nombre del producto',
                'id':'nombre'
            }),
            'descripcion':forms.Textarea(attrs={'class':'form-control'}),
            'precio':forms.NumberInput(attrs={'class':'form-control'}),
            'cantidad':forms.NumberInput(attrs={'class':'form-control'}),
            'categoria':forms.Select(attrs={'class':'form-control'}),
            'proveedor':forms.Select(attrs={'class':'form-control'}),
            'codigo':forms.TextInput(attrs={'class':'form-control'}),
            'activo':forms.CheckboxInput(attrs={'class':'form-check-input'}),
            'disponible':forms.CheckboxInput(attrs={'class':'form-check-input'}),


        }


