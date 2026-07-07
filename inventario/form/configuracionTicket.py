from django import forms
from inventario.models import ConfiguracionTicket
class ConfiguracionTicketForm(forms.ModelForm):

    class Meta:
        model = ConfiguracionTicket
        fields = "__all__"