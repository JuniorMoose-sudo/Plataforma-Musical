from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

'''Esta View direciona o usuário para a página de perfil após o login.'''

@login_required
def home(request):
    """
    Redireciona o usuário para a página de perfil após o login.
    """
    if request.user.is_professor:
        return redirect('painel_professor')
    return redirect('painel_aluno')

