# agenda/admin.py
from django.contrib import admin
from .models import AulaAgendada

@admin.register(AulaAgendada)
class AulaAgendadaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'professor', 'data', 'tipo', 'confirmada')
    list_filter = ('tipo', 'confirmada')
    search_fields = ('aluno__first_name', 'aluno__last_name')