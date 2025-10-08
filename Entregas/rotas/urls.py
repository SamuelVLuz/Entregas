from django.urls import path
from . import views

app_name = 'rotas'

urlpatterns = [
    path('rotas', views.upload_pdf, name='upload_pdf'),
    path('success', views.success, name='success'),

    path('listar', views.listar_rotas, name='listar_rotas'),
    path('detalhes/<int:rota_id>/', views.detalhes_rota, name='detalhes_rota'),
    path('excluir/<int:rota_id>/', views.excluir_rota, name='excluir_rota'),
    path('editar/<int:rota_id>/', views.editar_rota, name='editar_rota'),
    path('editar/<int:rota_id>/excluir/<int:entrega_id>/', views.excluir_entrega, name='excluir_entrega'),
    path('gerar_pdf/<int:rota_id>/', views.gerar_pdf_rota, name='gerar_pdf_rota'),
    path('mapa/<int:rota_id>/', views.mapa_rota, name='mapa_rota'),


]
