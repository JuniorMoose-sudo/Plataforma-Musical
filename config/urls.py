from django.contrib import admin
from django.urls import path, include


'''URL confgurações para o projeto Django.
   Inclui as URLs do admin, allauth e do aplicativo core.
   As URLs do aplicativo core são incluídas para gerenciar as páginas principais do site'''

urlpatterns = [
    path('admin/', admin.site.urls),
    path('aulas/', include('aulas.urls', namespace='aulas')), 
    path('usuarios/', include('usuarios.urls')),
    path('', include('core.urls')),
    path('accounts/', include('allauth.urls')),
    path('agenda/', include('agenda.urls', namespace='agenda')),

]