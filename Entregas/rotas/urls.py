from django.urls import path
from . import views

app_name = 'rotas'

urlpatterns = [
    path(views.upload_pdf, name='upload_pdf'),
]
