from django.db import models

class Entrega(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    cep = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=100)
    data_emissao = models.DateField()
    data_adicao = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{}, {}, {}, {}, {}, {}, {}, {}".format(self.nome, self.endereco, self.bairro, self.cep, self.cidade, self.uf, self.data_emissao, self.data_adicao)