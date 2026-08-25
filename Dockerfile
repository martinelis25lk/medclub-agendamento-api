# ==========================================
# STAGE 1: Builder (Compilação e Dependências)
# ==========================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Variáveis de ambiente para o Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências de sistema necessárias para compilar pacotes
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Cria o ambiente virtual e instala os pacotes
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ==========================================
# STAGE 2: Final (Imagem enxuta para Produção)
# ==========================================
FROM python:3.12-slim

WORKDIR /app

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala apenas as bibliotecas de runtime necessárias (ex: libpq)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copia a venv do Stage 1
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copia o código da aplicação
COPY . .

# BOAS PRÁTICAS: Cria e usa um usuário não-root por questões de segurança
RUN adduser --disabled-password --no-create-home appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expõe a porta que o Django usará
EXPOSE 8000

# Executa o servidor 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]