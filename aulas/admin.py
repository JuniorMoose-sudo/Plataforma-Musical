from django.contrib import admin
from .models import Aula, ProgressoAlunoAula

@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'mundo', 'professor', 'data_criacao')
    list_filter = ('categoria', 'mundo')
    search_fields = ('titulo', 'descricao')
    ordering = ('-data_criacao',)

@admin.register(ProgressoAlunoAula)
class ProgressoAlunoAulaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'aula', 'data_visualizacao')
    list_filter = ('data_visualizacao',)
