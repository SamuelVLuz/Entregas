from django import forms

class PDFUploadForm(forms.Form):
    title = forms.CharField(max_length=100)
    pdf_file = forms.FileField(label='Select a PDF file')