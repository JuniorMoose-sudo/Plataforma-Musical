# agenda/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import AulaAgendada
from django.core.exceptions import ValidationError

@receiver(pre_save, sender=AulaAgendada)
def validate_aula_horario(sender, instance, **kwargs):
    # Verifica conflitos de horário para o mesmo professor/aluno
    conflitos = AulaAgendada.objects.filter(
        professor=instance.professor,
        data__date=instance.data.date(),
        data__hour=instance.data.hour()
    ).exclude(pk=instance.pk)
    
    if conflitos.exists():
        raise ValidationError("Já existe uma aula agendada neste horário.")