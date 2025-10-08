from django.shortcuts import render, get_object_or_404, redirect

from rotas.models import Entrega
from rotas.models import Rota
from rotas.forms import pdf_form

def excluir_entrega(request, rota_id, entrega_id):
    rota = get_object_or_404(Rota, id=rota_id)
    entrega = get_object_or_404(Entrega, id=entrega_id)

    rota.entregas.remove(entrega)
    entrega.delete()

    return redirect('rotas:editar_rota', rota_id=rota.id)