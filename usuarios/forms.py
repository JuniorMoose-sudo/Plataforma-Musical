from django import forms
from allauth.account.forms import SignupForm

'''Este arquivo contém os formulários personalizados para o aplicativo de usuários.
   Aqui, você pode definir formulários adicionais ou modificar os existentes
   para atender às necessidades específicas do seu projeto.
   Certifique-se de que os formulários estejam registrados corretamente no Django Admin
   e que sejam utilizados nas views apropriadas.'''

class CustomSignupForm(SignupForm):
    is_professor = forms.BooleanField(required=False, label="É Professor?")

    def save(self, request):
        user = super().save(request)
        user.is_professor = self.cleaned_data.get('is_professor')
        user.save()
        return user