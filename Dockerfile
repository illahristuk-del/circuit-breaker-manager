FROM python:3.12-alpine AS builder

RUN apk add --no-cache build-base gcc musl-dev postgresql-dev libffi-dev

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt --prefix=/install

FROM python:3.12-alpine AS final

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

RUN apk add --no-cache libpq curl && \
    addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=builder /install /usr/local

COPY --chown=appuser:appgroup ./app /app/app
COPY --chown=appuser:appgroup ./migrations /app/migrations
COPY --chown=appuser:appgroup ./alembic.ini /app/alembic.ini

USER appuser

EXPOSE ${PORT}

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
