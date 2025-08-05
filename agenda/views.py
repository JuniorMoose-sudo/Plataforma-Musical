from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView
from .models import AulaAgendada
from .forms import AgendarAulaForm

class AgendarAulaView(LoginRequiredMixin, CreateView):
    model = AulaAgendada
    form_class = AgendarAulaForm
    template_name = 'agenda/agendar.html'
    success_url = reverse_lazy('agenda:aulas_professor')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['professor'] = self.request.user  # Passa o professor logado para o form
        return kwargs

class AulasProfessorView(LoginRequiredMixin, ListView):
    model = AulaAgendada
    template_name = 'agenda/aulas_professor.html'
    context_object_name = 'aulas'

    def get_queryset(self):
        return AulaAgendada.objects.filter(
            professor=self.request.user
        ).order_by('data')

class EditarAulaView(LoginRequiredMixin, UpdateView):
    model = AulaAgendada
    form_class = AgendarAulaForm
    template_name = 'agenda/editar_aula.html'
    success_url = reverse_lazy('agenda:aulas_professor')

class CancelarAulaView(LoginRequiredMixin, View):
    def post(self, request, pk):
        aula = get_object_or_404(AulaAgendada, pk=pk, professor=request.user)
        aula.delete()
        return redirect(reverse_lazy('agenda:aulas_professor'))