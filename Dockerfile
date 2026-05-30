# ── Stage 1: dependency builder ──────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# Install deps into a prefix so we can copy them cleanly
COPY app/requirements.txt .
RUN pip install --upgrade pip \
 && pip install --prefix=/install --no-cache-dir -r requirements.txt


# ── Stage 2: lean runtime image ──────────────────────────────────────────────
FROM python:3.12-slim

LABEL org.opencontainers.image.title="devops-webapp" \
      org.opencontainers.image.description="FastAPI app behind Nginx" \
      org.opencontainers.image.version="1.0.0"

WORKDIR /app

# Non-root user — security best practice
RUN addgroup --system app && adduser --system --ingroup app app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY app/ .

USER app

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
