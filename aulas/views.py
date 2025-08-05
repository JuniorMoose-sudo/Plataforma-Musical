# aulas/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Aula, ProgressoAlunoAula
from django.contrib.auth.decorators import login_required
from .forms import AulaAgendadaForm
from agenda.models import AulaAgendada
from .forms import AulaForm


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
    mundo = request.GET.get('mundo')
    categoria = request.GET.get('categoria')
    
    aulas = Aula.objects.all()
    if mundo:
        aulas = aulas.filter(mundo=mundo)
    if categoria:
        aulas = aulas.filter(categoria=categoria)

    assistidas_ids = ProgressoAlunoAula.objects.filter(aluno=request.user).values_list('aula_id', flat=True)
    
    return render(request, 'aulas/lista.html', {
        'aulas': aulas,
        'assistidas_ids': assistidas_ids
    })

@login_required
def assistir_aula(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)

    assistida = ProgressoAlunoAula.objects.filter(aluno=request.user, aula=aula).exists()

    return render(request, 'aulas/detalhe.html', {
        'aula': aula,
        'assistida': assistida
    })

@login_required
def marcar_como_assistida(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    progresso, created = ProgressoAlunoAula.objects.get_or_create(aluno=request.user, aula=aula)
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



