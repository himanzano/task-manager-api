# Task Manager API

Uma API RESTful para gerenciamento de tarefas, desenvolvida com FastAPI, PostgreSQL e SQLAlchemy 2.0. Este projeto demonstra práticas modernas de desenvolvimento backend, incluindo autenticação robusta, tipagem estrita e testes automatizados.

## 🚀 Visão Geral

A Task Manager API oferece uma plataforma segura para usuários gerenciarem suas tarefas pessoais. Funcionalidades principais:
- **Autenticação de Usuários**: Registro e login seguros usando JWT (Tokens de Acesso e Refresh).
- **Domínio de Tarefas**: CRUD completo com validação de propriedade (um usuário só acessa suas próprias tarefas).
- **Integridade de Dados**: Relacionamentos e restrições no nível do banco de dados.
- **Robustez Operacional**: Tratamento global de exceções, logs estruturados e endpoints de saúde (health check).

## 🛠️ Stack Tecnológica

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12+)
- **Banco de Dados**: [PostgreSQL](https://www.postgresql.org/)
- **ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Síncrono)
- **Migrações**: [Alembic](https://alembic.sqlalchemy.org/)
- **Autenticação**: JWT (Jose) + Bcrypt
- **Validação**: [Pydantic v2](https://docs.pydantic.dev/)
- **Testes**: [Pytest](https://docs.pytest.org/) + FastAPI TestClient
- **Gerenciador de Pacotes**: [uv](https://github.com/astral-sh/uv)

## 💡 Decisões Técnicas

### SQLAlchemy 2.0 e Engine Síncrona

Embora o FastAPI suporte operações assíncronas, optou-se por um driver síncrono (`psycopg2`) pela maturidade e robustez em fluxos de CRUD tradicionais. Utilizamos o novo estilo declarativo do SQLAlchemy 2.0 (`Mapped[]`, `mapped_column`) para garantir máxima compatibilidade com verificadores de tipo (Mypy/Pyright).

### Estratégia de Autenticação

Implementamos um sistema de **dois tokens**:

- **Access Token**: Curta duração (30 min) para autorizar requisições.
- **Refresh Token**: Longa duração (7 dias) para renovar a sessão sem exigir novas credenciais.
- **Bcrypt**: Senhas nunca são armazenadas em texto plano, utilizando um fator de custo adequado para produção.

### Padronização de Erros

Todas as exceções são capturadas por um manipulador global, garantindo que o cliente receba sempre o mesmo formato de resposta, evitando o vazamento de stack traces internos:
```json
{
  "message": "Descrição amigável do erro",
  "details": [...]
}
```

## 🏁 Como Rodar Localmente

### Pré-requisitos

- Python 3.12+
- PostgreSQL rodando localmente
- `uv` (recomendado) ou `pip`

### 1. Clonar o repositório

```bash
git clone https://github.com/himanzano/task-manager-api.git
cd task-manager-api
```

### 2. Configurar o ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/task_manager"
SECRET_KEY="sua_chave_secreta_super_segura"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 3. Instalar dependências

Com `uv`:

```bash
uv sync
```

### 4. Rodar as migrações

```bash
uv run alembic upgrade head
```

### 5. Popular ou Resetar o banco de dados (Opcional)

Para criar dados de exemplo (usuários e tarefas):
```bash
uv run scripts/seed.py
```

Para apagar todos os dados e resetar o banco:
```bash
uv run scripts/clean_db.py
```

### 6. Iniciar o servidor

```bash
uv run scripts/dev.py

# se preferir rode o comando diretamente:
# uv run uvicorn app.main:app --reload --port 8080
```

A API estará disponível em `http://localhost:8080`.

## 🔐 Como Autenticar

A API utiliza autenticação via **Bearer Token**.

1. **Registro**: Crie sua conta em `POST /auth/register`.
2. **Login**: Obtenha seus tokens em `POST /auth/login`.
3. **Autorização**: Em todas as rotas protegidas (ex: `/tasks`), envie o header:
   `Authorization: Bearer <seu_access_token>`

## 🧪 Testes

Para rodar a suíte de testes automatizados (utiliza SQLite em memória para isolamento total):

```bash
uv run pytest
```

## 🔍 Testes Manuais (Arquivos .http)

Além dos testes automatizados, o projeto inclui arquivos `.http` na pasta `http/` para facilitar o debugging e testes manuais rápidos.

### Como usar:

1. Instale a extensão **REST Client** no VS Code ou utilize a CLI [**httpyac**](https://github.com/AnWeber/httpyac).
2. Certifique-se de que a API está rodando.
3. Abra os arquivos em `http/`:
   - `auth.http`: Testes de registro, login e renovação de token.
   - `tasks.http`: CRUD completo de tarefas (possui fluxo dinâmico que captura o ID da tarefa criada).
   - `health.http`: Verificação de saúde da API.

*Nota: Os arquivos são dinâmicos. Ao executar o Login, o token é capturado automaticamente para as requisições subsequentes.*

## 📄 Documentação (Swagger)

A documentação interativa e completa pode ser acessada em:
`http://localhost:8080/docs`
