from django.urls import path
from . import views

app_name = 'rotas'

urlpatterns = [
    path('rotas/', views.upload_pdf, name='upload_pdf'),
]
