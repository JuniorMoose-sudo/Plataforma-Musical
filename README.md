🎵 Plataforma de Aulas de Música

Django + Python | Tailwind CSS | PostgreSQL

📌 Visão Geral

A Plataforma de Aulas de Música é um sistema web completo para gerenciar aulas gravadas, agendar aulas presenciais e acompanhar o progresso dos alunos.

Voltada para canto, teclado e órgão, ela oferece painéis distintos para alunos e professores, controle de agenda, progresso e organização por níveis (“mundos”).

💡 Objetivo: criar uma experiência de aprendizado musical organizada, intuitiva e acessível.

✨ Funcionalidades

👨‍🎓 Alunos

✅ Cadastro/Login com autenticação segura (Django Auth / django-allauth)

✅ Perfil com dados pessoais e histórico

✅ Escolha de mundos (níveis): Iniciante, Intermediário, Avançado (futuro)

✅ Acesso a aulas gravadas por categoria e nível

✅ Marcar aulas como assistidas e registrar progresso

✅ Visualizar agenda de aulas presenciais agendadas pelo professor

✅ Painel com resumo do progresso


👨‍🏫 Professores

✅ Painel exclusivo com permissões diferenciadas

✅ Cadastro e organização de aulas gravadas (YouTube)

✅ Agendamento de aulas presenciais para alunos

✅ Edição ou cancelamento de agendamentos

✅ Lista de alunos e (futuramente) acompanhamento de progresso

🛠 Stack Tecnológica
Camada	Tecnologia
#Backend	Django + (opcional DRF)
#Frontend	Django Templates + Tailwind CSS
#Banco de Dados	PostgreSQL
#Autenticação	Django Auth / django-allauth
#Vídeos	YouTube Embed / django-video
#Agendamentos	Modelos customizados

⚙️ Instalação
# 1️⃣ Clonar repositório
git clone https://github.com/seuusuario/plataforma-musical.git
cd plataforma-musical

# 2️⃣ Criar ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# 3️⃣ Instalar dependências
pip install -r requirements.txt

# 4️⃣ Configurar variáveis de ambiente
cp .env.example .env

# 5️⃣ Rodar migrações e criar superusuário
python manage.py migrate
python manage.py createsuperuser

# 6️⃣ Iniciar servidor
python manage.py runserver

🖼 Screenshots
📌 Login e Cadastro


📌 Painel do Aluno


📌 Painel do Professor


📌 Agendamento de Aulas

