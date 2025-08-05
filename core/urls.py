from django.urls import path
from .views import home

'''Esta URL direciona o usuário para a view home após o login.
'''

urlpatterns = [
    path('', home, name='home'),
]