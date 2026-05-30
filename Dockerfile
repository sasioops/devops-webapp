FROM python:3.12-slim AS builder
WORKDIR /build
COPY app/requirements.txt .
RUN pip install --upgrade pip \
 && pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
RUN addgroup --system app && adduser --system --ingroup app app
COPY --from=builder /install /usr/local
COPY app/ .
USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')"
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000", "--workers", "2"]