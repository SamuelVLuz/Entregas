from django.shortcuts import render
def home(request):
    context = {
        'nome' : "Samuel"
    }

    return render(request, 'conteudo.html', context)

def upload_pdf(request):
    return render(request, 'rotas/upload_pdf.html')
