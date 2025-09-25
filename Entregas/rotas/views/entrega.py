from django.shortcuts import render, get_object_or_404, redirect

from rotas.models import Entrega
from rotas.forms import pdf_form