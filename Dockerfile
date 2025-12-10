FROM cgr.dev/chainguard/python:latest-dev AS builder

# Copia o binário do uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copia arquivos de dependências
COPY pyproject.toml uv.lock ./

# Instala todas as dependências dentro de um venv gerenciado pelo uv
RUN uv sync --frozen --no-cache

# Copia o contéudo de src para /app
COPY src .

FROM cgr.dev/chainguard/python:latest

WORKDIR /app

# Copia app + venv pronto
COPY --from=builder /app /app

# Usa o ambiente virtual criado pelo uv
ENV PATH="/app/.venv/bin:${PATH}"

EXPOSE 8000

USER nonroot

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
