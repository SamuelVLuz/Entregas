from django.shortcuts import render, get_object_or_404, redirect
from rotas.models import Rota, Entrega
from rotas.forms.entregas_form import EntregasForm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.http import FileResponse
import io
from rotas.utils.ors_rotas import *

def listar_rotas(request):
    rotas = Rota.objects.all().order_by('-data_criacao')
    return render(request, 'rotas/listar_rotas.html', {'rotas': rotas})

def detalhes_rota(request, rota_id):
    rota = get_object_or_404(Rota, id=rota_id)
    entregas = rota.entregas.all()
    return render(request, 'rotas/detalhes_rota.html', {'rota': rota, 'entregas': entregas})

def excluir_rota(request, rota_id):
    rota = get_object_or_404(Rota, id=rota_id)
    rota.delete()
    return redirect('rotas:listar_rotas')

def editar_rota(request, rota_id):
    rota = get_object_or_404(Rota, id=rota_id)

    if request.method == 'POST':
        form = EntregasForm(request.POST)
        if form.is_valid():
            entrega = form.save()
            rota.entregas.add(entrega)
            return redirect('rotas:editar_rota', rota_id=rota.id)
    else:
        form = EntregasForm()

    entregas = rota.entregas.all()
    return render(request, 'rotas/editar_rota.html', {'rota': rota, 'entregas': entregas, 'form': form})

def gerar_pdf_rota(request, rota_id):
    rota = get_object_or_404(Rota, id=rota_id)
    entregas = list(rota.entregas.all())

    ordem, distancia = melhor_ordem_entregas_ors(entregas)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"Rota: {rota.nome}", styles['Heading1']))
    story.append(Paragraph(f"Distância total estimada: {distancia/1000:.2f} km", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Ordem sugerida de entregas:", styles['Heading2']))
    story.append(Spacer(1, 6))

    if not ordem:
        story.append(Paragraph("Nenhuma entrega com endereço válido foi encontrada.", styles['Normal']))
    else:
        for i, e in enumerate(ordem, start=1):
            story.append(Paragraph(f"<b>{i}. {e.nome}</b>", styles['Normal']))
            story.append(Paragraph(f"Endereço: {e.endereco}", styles['Normal']))
            story.append(Paragraph(f"Bairro: {e.bairro}", styles['Normal']))
            story.append(Paragraph(f"Cidade/UF: {e.cidade} - {e.uf}", styles['Normal']))
            story.append(Paragraph(f"CEP: {e.cep}", styles['Normal']))
            story.append(Paragraph(f"Data de emissão: {e.data_emissao}", styles['Normal']))
            story.append(Spacer(1, 8))

    doc.build(story)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"rota_{rota.id}.pdf")


def mapa_rota(request, rota_id):
    rota = get_object_or_404(Rota, id=rota_id)
    enderecos = [f"{e.endereco}, {e.cidade}, {e.uf}" for e in rota.entregas.all()]

    ordem, distancia = melhor_ordem_entregas_ors(enderecos)

    coordenadas = []
    for i, coord in enumerate(ordem, start=1):
        coordenadas.append({
            'index': i,
            'lat': coord[1],
            'lng': coord[0],
            'endereco': enderecos[i - 1]
        })

    contexto = {
        'rota': rota,
        'coordenadas': coordenadas,
        'distancia': round(distancia / 1000, 2),
    }
    return render(request, 'rotas/mapa_rota.html', contexto)

