import re
from django.core.exceptions import ValidationError
from django import forms
from agenda.models import AulaAgendada 
from django.contrib.auth.models import User
from .models import Aula 

class AulaAgendadaForm(forms.ModelForm):
    class Meta:
        model = AulaAgendada
        fields = ['data', 'aluno', 'tipo', 'observacoes']
        widgets = {
            'data': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get("data")
        aluno = cleaned_data.get("aluno")

        conflitos = AulaAgendada.objects.filter(data=data, aluno=aluno)
        if conflitos.exists():
            raise forms.ValidationError("Este aluno já possui uma aula nesse horário.")

class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ['titulo', 'descricao', 'url_video', 'mundo', 'categoria']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring focus:border-blue-300'
            })

    def clean_url_video(self):
        url = self.cleaned_data.get('url_video')
        padrao = r'(?:v=|\/embed\/|\.be\/)([A-Za-z0-9_-]{11})'
        match = re.search(padrao, url)
        if not match:
            raise ValidationError("URL do vídeo inválida ou ID do YouTube não encontrado.")
        self.cleaned_data['youtube_id'] = match.group(1)
        return url

    def save(self, commit=True):
        aula = super().save(commit=False)
        aula.youtube_id = self.cleaned_data.get('youtube_id')
        if commit:
            aula.save()
        return aula
