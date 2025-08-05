from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from aulas.models import Aula, ProgressoAlunoAula

'''Views para os painéis de usuário'''

@login_required
def painel_aluno(request):
    mundos = ['1', '2', '3']
    progresso_por_mundo = []

    for mundo in mundos:
        total = Aula.objects.filter(mundo=mundo).count()
        assistidas = ProgressoAlunoAula.objects.filter(aluno=request.user, aula__mundo=mundo).count()
        percent = 0
        if total > 0:
            percent = (assistidas / total) * 100

        progresso_por_mundo.append({
            'mundo': mundo,
            'assistidas': assistidas,
            'total': total,
            'percent': percent,
        })

    return render(request, 'usuarios/painel_aluno.html', {
        'progresso': progresso_por_mundo
    })


