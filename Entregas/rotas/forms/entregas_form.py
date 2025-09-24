from django import forms
from rotas.models import Entrega

class EntregasForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EntregasForm, self).__init__(*args, **kwargs)
        for new_field in self.visible_fields():
            new_field.field.widget.attrs['class'] = 'form-control'