# aulas/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Aula, ProgressoAlunoAula
from django.contrib.auth.decorators import login_required
from .forms import AulaAgendadaForm
from agenda.models import AulaAgendada
from .forms import AulaForm
from missoes.models import Missao, MissaoAluno


''' Este arquivo contém as views para o aplicativo de aulas, permitindo que os usuários visualizem, assistam e agendem aulas.
    - lista_aulas: Exibe uma lista de aulas filtradas por mundo e categoria.
    - assistir_aula: Permite que um aluno assista a uma aula específica e marque como assistida.
    - marcar_como_assistida: Marca uma aula como assistida para o aluno.
    - agendar_aula: Permite que professores agendem aulas com alunos.
    - lista_aulas_professor: Exibe as aulas agendadas para o professor.
    - lista_aulas_aluno: Exibe as aulas agendadas para o aluno.
    - detalhes_aula_agendada: Exibe os detalhes de uma aula agendada específica.'''

@login_required
def lista_aulas(request):
    mundo_id = request.GET.get('mundo')
    categoria = request.GET.get('categoria')

    assistidas_ids = ProgressoAlunoAula.objects.filter(
        aluno=request.user
    ).values_list('aula_id', flat=True)

    if mundo_id:
        mundo_id = int(mundo_id)
        mundo_str = str(mundo_id)

        # Verifica se todas as aulas do mundo 1 foram assistidas
        aulas_mundo_1 = Aula.objects.filter(mundo='1')
        aulas_assistidas_mundo_1 = aulas_mundo_1.filter(
            id__in=ProgressoAlunoAula.objects.filter(aluno=request.user).values_list('aula_id', flat=True)
        )
        mundo_1_completo = aulas_mundo_1.exists() and aulas_mundo_1.count() == aulas_assistidas_mundo_1.count()

        # Mundo 1 sempre está liberado sem verificação
        if mundo_id == 1:
            aulas = Aula.objects.filter(mundo=mundo_str)
            mundo_liberado = True
            bloqueado = False
            missoes = []

        else:
            # Bloqueio adicional: mundo 2 ou 3 só liberado se mundo 1 estiver completo
            if mundo_id in [2, 3] and not mundo_1_completo:
                bloqueado = True
                aulas = []
                mensagem = "Você precisa concluir todas as aulas do Mundo 1 antes de acessar este conteúdo."
                mundo_id_anterior = 1
                return render(request, 'aulas/bloqueado.html', {
                    'mensagem': mensagem,
                    'mundo_id_anterior': mundo_id_anterior
                })

            # Verificar missões para mundos > 1
            missoes = Missao.objects.filter(mundo=mundo_str)
            concluidas_ids = MissaoAluno.objects.filter(
                aluno=request.user,
                missao__in=missoes,
                concluida=True
            ).values_list('missao_id', flat=True)

            for m in missoes:
                m.concluida = m.id in concluidas_ids

            mundo_liberado = all(m.concluida for m in missoes)
            bloqueado = not mundo_liberado

            if bloqueado:
                aulas = []
            else:
                aulas = Aula.objects.filter(mundo=mundo_str)

        if categoria and aulas.exists():
            aulas = aulas.filter(categoria=categoria)

    else:
        aulas = Aula.objects.none()
        bloqueado = False
        missoes = []
        mundo_liberado = False

    return render(request, 'aulas/lista.html', {
        'aulas': aulas,
        'assistidas_ids': assistidas_ids,
        'bloqueado': bloqueado,
        'missoes': missoes,
        'mundo_id': mundo_id if mundo_id else None,
        'mundo_liberado': mundo_liberado
    })

@login_required
def assistir_aula(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)

    # Verifica se todas as aulas do mundo 1 foram assistidas
    aulas_mundo_1 = Aula.objects.filter(mundo='1')
    aulas_assistidas_mundo_1 = aulas_mundo_1.filter(
        id__in=ProgressoAlunoAula.objects.filter(aluno=request.user).values_list('aula_id', flat=True)
    )
    mundo_1_completo = aulas_mundo_1.exists() and aulas_mundo_1.count() == aulas_assistidas_mundo_1.count()

    # Mundo 1 sempre liberado
    if aula.mundo == '1':
        mundo_liberado = True

    # Mundos 2 e 3 exigem conclusão do mundo 1
    elif aula.mundo in ['2', '3'] and not mundo_1_completo:
        mensagem = "Você precisa concluir todas as aulas do Mundo 1 antes de acessar esta aula."
        mundo_id_anterior = 1
        return render(request, 'aulas/bloqueado.html', {
            'mensagem': mensagem,
            'mundo_id_anterior': mundo_id_anterior
        })

    else:
        # Verificar missões para outros mundos
        missoes = Missao.objects.filter(mundo=aula.mundo)
        concluidas = MissaoAluno.objects.filter(
            aluno=request.user,
            missao__in=missoes,
            concluida=True
        ).count()
        mundo_liberado = concluidas == missoes.count()

        if not mundo_liberado:
            mensagem = "Você precisa concluir todas as missões deste mundo antes de acessar esta aula."
            mundo_id_anterior = int(aula.mundo)
            return render(request, 'aulas/bloqueado.html', {
                'mensagem': mensagem,
                'mundo_id_anterior': mundo_id_anterior
            })

    assistida = ProgressoAlunoAula.objects.filter(aluno=request.user, aula=aula).exists()

    return render(request, 'aulas/detalhe.html', {
        'aula': aula,
        'assistida': assistida,
        'mundo_liberado': mundo_liberado
    })

@login_required
def marcar_como_assistida(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)

    # Marca aula como assistida
    progresso, created = ProgressoAlunoAula.objects.get_or_create(
        aluno=request.user,
        aula=aula
    )

    # Verifica se existe uma missão vinculada a essa aula
    missao = Missao.objects.filter(aula=aula).first()

    if missao:
        # Verifica se o aluno já concluiu essa missão
        missao_aluno, created = MissaoAluno.objects.get_or_create(
            aluno=request.user,
            missao=missao
        )

        if not missao_aluno.concluida:
            missao_aluno.concluida = True
            missao_aluno.save()

    return redirect('aulas:assistir_aula', aula_id=aula.id)

@login_required
def agendar_aula(request):
    if not request.user.groups.filter(name='Professores').exists():
        return redirect('home')

    if request.method == 'POST':
        form = AulaAgendadaForm(request.POST)
        if form.is_valid():
            nova_aula = form.save(commit=False)
            nova_aula.professor = request.user
            nova_aula.save()
            return redirect('lista_aulas_professor')
    else:
        form = AulaAgendadaForm()

    return render(request, 'aulas/agendar_aula.html', {'form': form})

@login_required
def detalhe_aula(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    return render(request, 'aulas/detalhe_aula.html', {'aula': aula})

@login_required
def painel_professor(request):
    aulas = AulaAgendada.objects.filter(professor=request.user).order_by('data')
    return render(request, 'aulas/painel_professor.html', {'aulas': aulas})

@login_required
def painel_aluno_agenda(request):
    aulas = AulaAgendada.objects.filter(aluno=request.user).order_by('data')
    return render(request, 'aulas/painel_aluno_agenda.html', {'aulas': aulas})

@login_required
def nova_aula(request):
    if request.method == 'POST':
        form = AulaForm(request.POST)
        if form.is_valid():
            aula = form.save(commit=False)
            aula.professor = request.user
            aula.save()
            return redirect('aulas:lista_aulas')
    else:
        form = AulaForm()

    return render(request, 'aulas/nova_aula.html', {'form': form})