from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tipo(models.Model):
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Tipo'

    def __str__(self):
        return self.nome

class Verif(models.Model):
    cpf_cnpj = models.CharField(max_length=255)
    

    class Meta:
        verbose_name_plural = 'Verificação'

    def __str__(self):
        return self.cpf_cnpj