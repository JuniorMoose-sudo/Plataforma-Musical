from django.db import models
from django.conf import settings
from aulas.models import Aula

MUNDOS = [
    ('1', 'Mundo 1'),
    ('2', 'Mundo 2'),
    ('3', 'Mundo 3'),
]

class Missao(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    aula = models.ForeignKey(Aula, null=True, blank=True, on_delete=models.SET_NULL)
    mundo = models.CharField(max_length=1, choices=MUNDOS)
    ordem = models.IntegerField(default=0)


class MissaoAluno(models.Model):
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    missao = models.ForeignKey(Missao, on_delete=models.CASCADE)
    concluida = models.BooleanField(default=False)
    data_conclusao = models.DateTimeField(auto_now_add=True)