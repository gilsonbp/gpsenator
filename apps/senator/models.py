from django.db import models

__author__ = "Gilson Paulino"
__date__ = "Created by 24/03/18"
__copyright__ = "Copyright 2018"
__email__ = "gilsonbp@gmail.com"


class Parliamentarian(models.Model):
    """
    Model of the parliamentarian.
    Using fields similar to those returned on the endpoint.
    """
    codigo = models.IntegerField(verbose_name='Código', primary_key=True)
    nome = models.CharField(max_length=250, verbose_name='Nome', null=True)
    nome_completo = models.CharField(
        max_length=250, verbose_name='Nome Completo', null=True)
    sexo = models.CharField(max_length=250, verbose_name='Sexo', null=True)
    forma_tratamento = models.CharField(
        max_length=100, verbose_name='Forma de Tratamento', null=True)
    url_foto = models.CharField(max_length=255, verbose_name='Foto', null=True)
    url_pagina = models.CharField(
        max_length=255, verbose_name='Página', null=True)
    email = models.EmailField(verbose_name='E-mail', null=True)
    sigla_partido = models.CharField(
        max_length=20, verbose_name='Sigla do Partido', null=True)
    uf = models.CharField(max_length=2, verbose_name='UF', null=True)
    glossario = models.CharField(
        max_length=255, verbose_name='Glossário', null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Parliamentarian'
        verbose_name_plural = 'Parliamentarians'
        permissions = (
            ('update_parliamentarians', 'Update Parliamentarians'),
        )
