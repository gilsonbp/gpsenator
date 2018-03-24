import requests
import json

from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.urls import path
from django.utils.decorators import method_decorator

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


@admin.register(Mandate)
class MandateAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'parliamentarian', 'descricao_participacao', 'uf']
    list_display_links = list_display
    search_fields = ['codigo', 'parliamentarian__nome', 'parliamentarian__nome_completo', 'parliamentarian__sigla_partido']
    list_filter = ['descricao_participacao', 'parliamentarian__sigla_partido', 'uf']
    list_per_page = 40
    autocomplete_fields = ['parliamentarian']