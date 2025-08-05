from django.db import models
from django.contrib.auth.models import AbstractUser

'''Modelo de Usuario
Esse modelo estende o modelo AbstractUser do Django para incluir um campo adicional
is_professor, que indica se o usuário é um professor ou não.
Esse campo é um BooleanField que, por padrão, é definido como False.
Esse modelo pode ser usado para gerenciar usuários em um sistema onde 
é necessário distinguir entre professores e outros tipos de usuários.
'''
class Usuario(AbstractUser):
    tipo = models.CharField(max_length=10, choices=[('ALUNO', 'Aluno'), ('PROFESSOR', 'Professor')])

    @property
    def is_professor(self):
        return self.tipo == 'PROFESSOR'

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

        
