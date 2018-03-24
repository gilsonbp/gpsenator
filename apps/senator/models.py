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


class Mandate(models.Model):
    """
    Model of the mandate.
    Using fields similar to those returned on the endpoint.
    """
    parliamentarian = models.ForeignKey(
        Parliamentarian, verbose_name='Parliamentarian', on_delete=models.CASCADE)
    codigo = models.IntegerField(verbose_name='Código', primary_key=True)
    uf = models.CharField(max_length=2, verbose_name='UF', null=True)
    pl_numero = models.IntegerField('Número Primeira Legislatura', null=True)
    pl_data_inicio = models.DateField(
        verbose_name='Data Início Primeira Legislatura', null=True)
    pl_data_fim = models.DateField(
        verbose_name='Data Fim Primeira Legislatura', null=True)
    sl_numero = models.IntegerField('Número Segunda Legislatura', null=True)
    sl_data_inicio = models.DateField(
        verbose_name='Data Início Segunda Legislatura', null=True)
    sl_data_fim = models.DateField(
        verbose_name='Data Fim Segunda Legislatura', null=True)
    descricao_participacao = models.CharField(
        max_length=100, verbose_name='Descrição Participação', null=True)
    t_descricao_participacao = models.CharField(max_length=100, verbose_name='Descrição Participação (Titular)',
                                                null=True)
    t_codigo_parlamentar = models.IntegerField(
        verbose_name='Código Parlamentar (Titular)', null=True)
    t_nome_parlamentar = models.CharField(
        max_length=250, verbose_name='Nome Parlamentar (Titular)', null=True)

    def __str__(self):
        return '%s - %s' % (self.codigo, self.parlamentar.nome)

    class Meta:
        verbose_name = 'Mandate'
        verbose_name_plural = 'Mandates'


class Alternate(models.Model):
    """
    Model of the Alternate.
    Using fields similar to those returned on the endpoint.
    """
    mandate = models.ForeignKey(
        Mandate, verbose_name='Mandate', on_delete=models.CASCADE)
    codigo_parlamentar = models.IntegerField(
        verbose_name='Código Parlamentar', null=True)
    descricao_participacao = models.CharField(
        max_length=100, verbose_name='Descrição Participação', null=True)
    nome_parlamentar = models.CharField(
        max_length=250, verbose_name='Nome Parlamentar', null=True)

    def __str__(self):
        return '%s - %s' % (self.nome_parlamentar, self.descricao_participacao)

    class Meta:
        unique_together = ('mandate', 'codigo_parlamentar')
        verbose_name = 'Alternate'
        verbose_name_plural = 'Alternates'
