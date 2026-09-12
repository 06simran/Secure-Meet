# ── Builder stage ─────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ── Runtime stage ──────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Runtime deps only
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Download NLTK data
RUN python -c "import nltk; nltk.download('stopwords',quiet=True); nltk.download('wordnet',quiet=True); nltk.download('punkt',quiet=True)"

# Copy app
COPY . .

# Train model at build time using sample data
RUN python ml/train_model.py

EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:5000/api/health || exit 1

CMD ["gunicorn", "app:create_app()", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "2", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
