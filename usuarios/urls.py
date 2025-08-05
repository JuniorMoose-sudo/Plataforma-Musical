from django.urls import path
from . import views
from aulas.views import painel_professor

urlpatterns = [
    path('painel/aluno/', views.painel_aluno, name='painel_aluno'),
    path('painel/professor/', painel_professor, name='painel_professor'),
]
