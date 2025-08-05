# agenda/urls.py
from django.urls import path
from .views import (
    AgendarAulaView,
    AulasProfessorView,
    EditarAulaView,
    CancelarAulaView,
)

app_name = 'agenda'

urlpatterns = [
    path('agendar/', AgendarAulaView.as_view(), name='agendar'),
    path('aulas-professor/', AulasProfessorView.as_view(), name='aulas_professor'),
    path('editar/<int:pk>/', EditarAulaView.as_view(), name='editar'),
    path('cancelar/<int:pk>/', CancelarAulaView.as_view(), name='cancelar'),
    path('minhas-aulas/', AulasProfessorView.as_view(), name='minhas_aulas'),
    
]