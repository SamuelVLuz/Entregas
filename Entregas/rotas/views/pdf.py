from django.shortcuts import render, redirect
from rotas.forms.pdf_form import PDFUploadForm
from django.core.files.storage import FileSystemStorage
from rotas.models import Entrega, Rota
from rotas.utils.pdf_extractor import extrair_campos_pdf


def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            files = request.FILES.getlist('pdf_files')

            # Cria a rota
            rota = Rota.objects.create(nome=title)

            fs = FileSystemStorage()
            for f in files:
                filename = fs.save(f.name, f)
                path = fs.path(filename)  # caminho no disco

                # Extrai os campos do PDF
                campos = extrair_campos_pdf(path)

                # Cria a entrega (sem campo 'rota')
                entrega = Entrega.objects.create(
                    nome=campos.get('nome') or 'Não identificado',
                    endereco=campos.get('endereco') or 'Não informado',
                    bairro=campos.get('bairro') or 'Não informado',
                    cep=campos.get('cep') or '00000000',
                    cidade=campos.get('cidade') or 'Não informada',
                    uf=campos.get('uf') or 'NA',
                    data_emissao=campos.get('data_emissao') or None,
                )

                # Adiciona a entrega à rota (ManyToMany)
                rota.entregas.add(entrega)

            return redirect('rotas:success')
    else:
        form = PDFUploadForm()

    return render(request, 'rotas/upload_pdf.html', {'form': form})

def success(request):
    return render(request, 'rotas/success.html')
