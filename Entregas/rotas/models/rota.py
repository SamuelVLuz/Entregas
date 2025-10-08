from django.db import models

class Rota(models.Model):
    nome = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)
    entregas = models.ManyToManyField('Entrega', related_name='rotas')

    def __str__(self):
        return f"{self.nome} ({self.data_criacao})"