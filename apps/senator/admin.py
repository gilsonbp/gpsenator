import requests
import json

from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.urls import path
from django.utils.decorators import method_decorator

from apps.senator.import_senators import ImportSenatorJSON
from apps.senator.models import (Parliamentarian, Mandate, Alternate, Exercise)

__author__ = "Gilson Paulino"
__date__ = "Created by 24/03/18"
__copyright__ = "Copyright 2018"
__email__ = "gilsonbp@gmail.com"

admin.site.site_header = 'GP Senator'
admin.site.site_title = 'GP Senator'
admin.site.index_title = 'DashBoard'

AuthenticationForm.base_fields['username'].widget.attrs['autocomplete'] = 'off'
AuthenticationForm.base_fields['password'].widget.attrs['autocomplete'] = 'off'


@admin.register(Parliamentarian)
class ParliamentarianAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'sigla_partido', 'uf']
    list_display_links = list_display
    search_fields = ['codigo', 'nome', 'nome_completo', 'sigla_partido']
    list_filter = ['sigla_partido', 'uf']
    list_per_page = 40

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update-parliamentarians', self.update_parliamentarians,
                 name='update_parliamentarians'),
        ]
        return my_urls + urls

    @method_decorator(permission_required('senator.update_parliamentarians', raise_exception=True))
    def update_parliamentarians(self, request):
        url = "http://legis.senado.gov.br/dadosabertos/senador/lista/atual"
        headers = {
            'Accept': "application/json",
        }
        response = requests.request("GET", url, headers=headers)
        jsonresponse = json.loads(response.text)

        rows = ImportSenatorJSON.parliamentarian(jsonresponse)

        self.message_user(
            request, 'Update performed successfully!', messages.SUCCESS)
        self.message_user(
            request, '%s parliamentarians were imported.' % rows, messages.INFO)
        return redirect('admin:senator_parliamentarian_changelist')


@admin.register(Mandate)
class MandateAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'parliamentarian',
                    'descricao_participacao', 'uf']
    list_display_links = list_display
    search_fields = ['codigo', 'parliamentarian__nome',
                     'parliamentarian__nome_completo', 'parliamentarian__sigla_partido']
    list_filter = ['descricao_participacao',
                   'parliamentarian__sigla_partido', 'uf']
    list_per_page = 40
    autocomplete_fields = ['parliamentarian']


@admin.register(Alternate)
class AlternateAdmin(admin.ModelAdmin):
    list_display = ['codigo_parlamentar',
                    'nome_parlamentar', 'descricao_participacao']
    list_display_links = list_display
    search_fields = ['codigo_parlamentar',
                     'nome_parlamentar', 'descricao_participacao']
    list_per_page = 40
    autocomplete_fields = ['mandate']


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'mandate', 'data_inicio', 'data_fim']
    list_display_links = list_display
    search_fields = ['codigo', 'mandate__parliamentarian__nome',
                     'mandate__parliamentarian__nome_completo']
    list_per_page = 40
    autocomplete_fields = ['mandate']
