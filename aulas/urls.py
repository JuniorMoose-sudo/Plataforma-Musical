from django.urls import path
from . import views

app_name = 'aulas'

urlpatterns = [
    path('', views.lista_aulas, name='lista_aulas'),
    path('<int:aula_id>/assistir/', views.assistir_aula, name='assistir_aula'),
    path('<int:aula_id>/assistida/', views.marcar_como_assistida, name='marcar_como_assistida'),
    path('aluno/agenda/', views.painel_aluno_agenda, name='painel_aluno_agenda'),
    path('agendar-aula/', views.agendar_aula, name='agendar_aula'),
    path('painel-professor/', views.painel_professor, name='painel_professor'),
    path('nova/', views.nova_aula, name='nova_aula'),
    path('<int:aula_id>/', views.detalhe_aula, name='detalhe_aula'),

    
]
