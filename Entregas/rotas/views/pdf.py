from django.shortcuts import render, redirect
from rotas.forms.pdf_form import PDFUploadForm
from django.core.files.storage import FileSystemStorage

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            files = request.FILES.getlist('pdf_files')

            fs = FileSystemStorage()

            for f in files:
                filename = fs.save(f.name, f)
                # Exemplo: salvando cada arquivo no modelo Entrega
                Entrega.objects.create(titulo=title, arquivo=filename)

            return redirect('rotas:success_page')  # redirecione como desejar
    else:
        form = PDFUploadForm()
    return render(request, 'rotas/upload_pdf.html', {'form': form})
