from django import forms
from rotas.models import Entrega
from django.forms.widgets import FileInput

class MultiplePDFInput(forms.ClearableFileInput):
    allow_multiple_selected = True  # permite múltiplos arquivos


class MultiplePDFField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultiplePDFInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        # Permite validar lista de arquivos
        if not data:
            return []
        if isinstance(data, (list, tuple)):
            return data
        return [data]


class PDFUploadForm(forms.Form):
    title = forms.CharField(max_length=100)
    pdf_files = MultiplePDFField(label="Selecione arquivos PDF")