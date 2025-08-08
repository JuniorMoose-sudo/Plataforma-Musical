from django.urls import path
from . import views

app_name = 'missoes'

urlpatterns = [
    path('<int:mundo_id>/', views.lista_missoes, name='lista'),
    path('concluir/<int:missao_id>/', views.concluir_missao, name='concluir_missao'),
]