# Guia de Deploy no Google Cloud Run

Esta aplicação foi containerizada e otimizada para execução no Google Cloud Run, utilizando Supabase (PostgreSQL) como banco de dados.

## 🌍 Variáveis de Ambiente

As seguintes variáveis de ambiente **DEVEM** ser configuradas na sua revisão do Cloud Run:

| Variável | Descrição | Exemplo |
|---|---|---|
| `DATABASE_URL` | String de conexão para o Supabase (Recomendado usar Connection Pooling). | `postgresql://postgres:[SENHA]@[HOST]:6543/postgres?sslmode=require` |
| `SECRET_KEY` | Segredo de alta entropia para assinatura de JWT. | `openssl rand -hex 32` |
| `ALGORITHM` | Algoritmo de criptografia (padrão: HS256). | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tempo de vida do token de acesso. | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Tempo de vida do token de atualização. | `7` |
| `ENV` | Nome do ambiente. | `production` |

> **Nota:** NÃO inclua arquivos `.env` na imagem do seu container.

## 🗄️ Migrações de Banco de Dados

As migrações são gerenciadas pelo Alembic e **não devem** ser executadas automaticamente na inicialização do container para evitar condições de corrida em ambientes escaláveis.

### Opção 1: Rodar Localmente (Recomendado para MVP)
Conecte-se à sua instância do Supabase a partir da sua máquina local e execute:
```bash
# Configure a URL do banco remoto
export DATABASE_URL="postgresql://postgres:[SENHA]@[HOST]:6543/postgres?sslmode=require"
uv run alembic upgrade head
```

### Opção 2: Cloud Build / GitHub Actions
Adicione uma etapa no seu pipeline de CI/CD para executar as migrações usando um container transiente antes de implantar a nova revisão.

## 🚀 Passos para Deploy

1. **Construir a imagem:**
   ```bash
   gcloud builds submit --tag gcr.io/[PROJECT-ID]/task-manager-api
   ```

2. **Implantar no Cloud Run:**
   ```bash
   gcloud run deploy task-manager-api \
     --image gcr.io/[PROJECT-ID]/task-manager-api \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars DATABASE_URL=...,SECRET_KEY=...
   ```
