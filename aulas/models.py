from django.db import models
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class Aula(models.Model):
    MUNDOS = [
        ('1', 'Mundo 1'),
        ('2', 'Mundo 2'),
        ('3', 'Mundo 3'),
    ]

    CATEGORIAS = [
        ('Tecnica Vocal', 'Técnica Vocal'),
        ('Teclado Arranjador', 'Teclado Arranjador'),
        ('Orgão', 'Órgão'),
        ('Violão', 'Violão'),
    ]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    url_video = models.URLField()
    mundo = models.CharField(max_length=1, choices=MUNDOS)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    professor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titulo} - {self.get_mundo_display()}'

    def youtube_id(self):
        match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", self.url_video)
        return match.group(1) if match else None

class ProgressoAlunoAula(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    data_visualizacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('aluno', 'aula')  # Um aluno só pode assistir a mesma aula uma vez

    def __str__(self):
        return f'{self.aluno.username} assistiu {self.aula.titulo}'
