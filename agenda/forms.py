from django import forms
from .models import AulaAgendada
from usuarios.models import Usuario  # Usando o modelo específico de usuário

class AgendarAulaForm(forms.ModelForm):
    class Meta:
        model = AulaAgendada
        fields = ['aluno', 'data', 'tipo', 'observacoes']
        widgets = {
            'data': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        self.professor = kwargs.pop('professor', None)
        super().__init__(*args, **kwargs)

        # Filtra apenas alunos ativos usando o modelo Usuario
        self.fields['aluno'].queryset = Usuario.objects.filter(
            tipo='ALUNO',
            is_active=True
        ).order_by('first_name')

        # Adiciona classe CSS 'form-control' aos campos
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.professor = self.professor  # Define o professor logado
        if commit:
            instance.save()
        return instance