from django.db import models
from django.contrib.auth import get_user_model
from aulas.models import Aula

User = get_user_model()

class AulaAgendada(models.Model):
    TIPO_AULA_CHOICES = [
        ('CANTO', 'Canto'),
        ('TECLADO', 'Teclado'),
        ('ORGAO', 'Órgão'),
    ]

    aluno = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'tipo': 'ALUNO'},  # Filtra apenas alunos
        related_name='aulas_agendadas_aluno'
    )
    professor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'tipo': 'PROFESSOR'},  # Filtra apenas professores
        related_name='aulas_agendadas_professor'
    )
    data = models.DateTimeField()
    tipo = models.CharField(max_length=10, choices=TIPO_AULA_CHOICES)
    observacoes = models.TextField(blank=True)
    confirmada = models.BooleanField(default=False)

    class Meta:
        ordering = ['data']
        verbose_name = 'Aula Agendada'
        verbose_name_plural = 'Aulas Agendadas'

    def __str__(self):
        return f"{self.tipo} - {self.aluno.get_full_name()} ({self.data.strftime('%d/%m/%Y %H:%M')})"