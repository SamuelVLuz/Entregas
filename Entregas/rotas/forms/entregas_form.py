from django import forms
from rotas.models import Entrega

class EntregasForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = ['nome', 'endereco', 'bairro', 'cep', 'cidade', 'uf', 'data_emissao']
        widgets = {
            'data_emissao': forms.DateInput(attrs={'type': 'date'}),
        }
