# Task Manager API

Uma API RESTful para gerenciamento de tarefas, desenvolvida com FastAPI, PostgreSQL e SQLAlchemy 2.0. Este projeto demonstra práticas modernas de desenvolvimento backend, incluindo autenticação robusta, tipagem estrita, testes automatizados e prontidão para deploy em nuvem (Cloud Run).

## 🚀 Visão Geral

A Task Manager API oferece uma plataforma segura para usuários gerenciarem suas tarefas pessoais. Funcionalidades principais:

- **Identificadores Únicos (UUID)**: Todas as entidades utilizam UUID v4 para maior segurança e escalabilidade.
- **Autenticação de Usuários**: Registro e login seguros usando JWT (Tokens de Acesso e Refresh).
- **Domínio de Tarefas**: CRUD completo com validação de propriedade (um usuário só acessa suas próprias tarefas).
- **Integridade e Auditoria**: Rastreamento automático de criação (`created_at`) e atualização (`updated_at`) via triggers no banco de dados.
- **Robustez Operacional**: Tratamento global de exceções, logs estruturados, CORS configurável e endpoints de saúde.

## 🛠️ Stack Tecnológica

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12+)
- **Banco de Dados**: [PostgreSQL](https://www.postgresql.org/)
- **ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Estilo Declarativo Moderno)
- **Migrações**: [Alembic](https://alembic.sqlalchemy.org/)
- **Autenticação**: JWT (Jose) + Bcrypt (Passlib)
- **Validação**: [Pydantic v2](https://docs.pydantic.dev/)
- **Testes**: [Pytest](https://docs.pytest.org/)
- **Ambiente/Build**: [uv](https://github.com/astral-sh/uv) e [Docker](https://www.docker.com/)

## 💡 Decisões Técnicas

### Identificadores UUID

Migramos de `Integer` para `UUID` como chaves primárias para evitar enumeração de recursos e facilitar integrações futuras em sistemas distribuídos.

### Lógica no Banco de Dados (Triggers)

Para garantir a integridade dos dados de auditoria, utilizamos triggers e funções PL/pgSQL nativas do PostgreSQL para gerenciar o campo `updated_at`, garantindo que a data seja atualizada mesmo se a alteração vier de fora da aplicação.

### Prontidão para Produção

A aplicação foi configurada pensando em ambientes serverless (como Google Cloud Run):

- Configurações via variáveis de ambiente com Pydantic Settings.
- Suporte a `SSL_MODE` para conexões seguras (essencial para Supabase/Cloud SQL).
- Gerenciamento de pool de conexões otimizado.
- CORS configurável para integração com frontends específicos.

## 🏁 Como Rodar Localmente

### Pré-requisitos

- Python 3.12+
- Docker e Docker Compose (Recomendado)
- `uv` (opcional, para rodar sem Docker)

### Opção A: Usando Docker (Mais Rápido)

O projeto inclui um `docker-compose.yml` que configura tanto o banco de dados quanto a API.

1. **Subir os serviços**:

   ```bash
   docker compose up -d
   ```

2. **Rodar as migrações**:

   ```bash
   docker compose exec api alembic upgrade head
   ```

A API estará disponível em `http://localhost:8080`.

### Opção B: Rodando Manualmente

1. **Configurar o ambiente**:
   Crie um arquivo `.env` baseado no `.env.example`:

   ```env
   DATABASE_URL="postgresql://postgres:postgres@localhost:5432/task_manager"
   SSL_MODE="disable"
   SECRET_KEY="sua_chave_secreta_super_segura"
   BACKEND_CORS_ORIGINS="http://localhost:3000,http://localhost:8080"
   ```

2. **Instalar dependências e rodar**:

   ```bash
   uv sync
   uv run alembic upgrade head
   uv run scripts/dev.py
   ```

## 🧪 Scripts Utilitários

- **Popular Banco**: `uv run scripts/seed.py` (Cria usuários e tarefas de teste)
- **Limpar Banco**: `uv run scripts/clean_db.py` (Apaga todos os registros)

## 🧪 Testes

Para rodar a suíte de testes automatizados:

```bash
uv run pytest
```

## 🔍 Testes Manuais (Arquivos .http)

O projeto inclui arquivos `.http` na pasta `http/` para uso com a extensão **REST Client** (VS Code).

- `auth.http`: Fluxo de autenticação.
- `tasks.http`: Operações de tarefas.
- `health.http`: Verificação de status.

## 📄 Documentação (Swagger)

Acesse a documentação interativa em:
`http://localhost:8080/docs`
