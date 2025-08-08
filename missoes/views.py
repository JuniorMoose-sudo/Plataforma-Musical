from django.shortcuts import render
from .models import Missao, MissaoAluno
from django.contrib.auth.decorators import login_required


# Dicionário pra exibir nome dos mundos
MUNDOS = {
    '1': 'Mundo 1',
    '2': 'Mundo 2',
    '3': 'Mundo 3',
}

def lista_missoes(request, mundo_id):
    mundo_str = str(mundo_id)
    missoes = Missao.objects.filter(mundo=str(mundo_id))

    concluidas = MissaoAluno.objects.filter(
        aluno=request.user,
        missao__in=missoes,
        concluida=True
    ).values_list('missao_id', flat=True)

    for missao in missoes:
        missao.concluida = missao.id in concluidas

    return render(request, 'missoes/missoes.html', {
        'missoes': missoes,
        'mundo_nome': MUNDOS.get(mundo_str, f"Mundo {mundo_str}")
    })

@login_required
def concluir_missao(request, missao_id):
    missao = get_object_or_404(Missao, id=missao_id)

    MissaoAluno.objects.get_or_create(
        aluno=request.user,
        missao=missao,
        defaults={'concluida': True}
    )

    # Ou se já existe, apenas marca como concluída
    MissaoAluno.objects.filter(
        aluno=request.user,
        missao=missao
    ).update(concluida=True)

    return redirect('lista_missoes', mundo_id=missao.mundo.id)