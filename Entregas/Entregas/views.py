from django.shortcuts import render
def home(request):
    context = {
        'nome' : "Samuel"
    }

    return render(request, 'conteudo.html', context)