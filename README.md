# API de Agendamento - Medclub

API RESTful desenvolvida em Django para gestão de especialistas, agendas e agendamentos de consultas, garantindo a distribuição automática de horários e a prevenção de reservas duplicadas.

##  Tecnologias Utilizadas
* **Python 3.12** & **Django / Django REST Framework**
* **PostgreSQL**
* **Docker & Docker Compose** (Multi-stage build focado em segurança)
* **Autenticação JWT** (`djangorestframework-simplejwt`)
* **Swagger** (`drf-yasg`) para documentação interativa

##  Como Executar o Projeto

1. Clone o repositório:

git clone https://github.com/martinelis25lk/medclub-agendamento-api.git


2. Suba a infraestrutura com Docker Compose:

docker-compose up -d --build


3. Acesse o container da aplicação para rodar as migrações e criar o usuário administrador:

docker exec -it medclub_web bash
python manage.py migrate
python manage.py createsuperuser

> ATENÇÃO O `createsuperuser` cria um usuário com acesso ao Django Admin, mas **não** define automaticamente o papel de negócio `interno`. Após criar, ajuste manualmente:
> ```
> python manage.py shell -c "from django.contrib.auth import get_user_model; U = get_user_model(); u = U.objects.get(username='SEU_USUARIO'); u.role = 'interno'; u.save()"
> ```


##  Documentação da API
Com o servidor rodando, acesse a documentação visual e teste as rotas em:
* **Swagger UI:** `http://localhost:8000/swagger/`

## Autenticação e Regras de Negócio
* **JWT com Roles:** O sistema distingue usuários `cliente` e `interno`. Rotas de gerenciamento (Especialistas e Agendas) exigem permissão de usuário interno.
* **Geração Automática de Slots:** Ao cadastrar uma nova Agenda, o sistema calcula e distribui de forma equidistante os horários de atendimento.
* **Testes Unitários:** As regras vitais (geração de slots e bloqueio de agendamento duplicado) estão 100% cobertas por testes automatizados (`python manage.py test`).


## Rotas da API

| Método | Rota | Acesso | Descrição |
|---|---|---|---|
| POST | `/api/auth/register/` | Público | Cadastro de cliente |
| POST | `/api/auth/token/` | Público | Login (retorna JWT) |
| POST | `/api/auth/token/refresh/` | Público | Renova o access token |
| GET/POST | `/api/especialistas/` | Leitura pública / Escrita interno | Cadastro de especialistas |
| GET/POST | `/api/agendas/` | Leitura pública / Escrita interno | Cadastro de agendas (gera horários automaticamente) |
| GET | `/api/horarios/` | Público | Lista horários disponíveis (somente leitura) |
| GET/POST | `/api/agendamentos/` | Autenticado | Lista (escopado ao usuário) e cria agendamentos |


## Convenção de Commits
Este projeto segue [Conventional Commits](https://www.conventionalcommits.org/):
`feat:` novas funcionalidades · `fix:` correções · `chore:` configuração/manutenção · `test:` testes · `ci:` integração contínua · `refactor:` melhorias sem mudança de comportamento



## Frontend (Vue)

1. Entre na pasta do frontend:

cd medclub-frontend

npm install

npm run dev

npm run dev

2. Acesse `http://localhost:5173`

3. Cadastre-se como cliente em `/registrar`, ou faça login se já tiver conta