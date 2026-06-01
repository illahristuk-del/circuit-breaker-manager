# --- РЎРўРђР”Р†РЇ Р—Р‘Р†Р РљР Р—РђР›Р•Р–РќРћРЎРўР•Р™ (РўРµРїРµСЂ С‚РµР¶ РЅР° Alpine) ---
FROM python:3.12-alpine AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /build

# Р’СЃС‚Р°РЅРѕРІР»СЋС”РјРѕ С–РЅСЃС‚СЂСѓРјРµРЅС‚Рё РєРѕРјРїС–Р»СЏС†С–С—, СЃРїРµС†РёС„С–С‡РЅС– РґР»СЏ Alpine (musl-dev Р·Р°РјС–СЃС‚СЊ glibc)
RUN apk add --no-cache build-base gcc musl-dev postgresql-dev libffi-dev

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt


# --- РЎРўРђР”Р†РЇ Р¤Р РћРќРўР•РќР”РЈ (Р—Р°РіР»СѓС€РєР° Р·Р° РўР—) ---
FROM alpine:latest AS frontend-builder
WORKDIR /frontend


# --- Р¤Р†РќРђР›Р¬РќРР™ РћР‘Р РђР— ---
FROM python:3.12-alpine AS final

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

# libpq РїРѕС‚СЂС–Р±РЅР° РґР»СЏ СЂРѕР±РѕС‚Рё РїСЃРёС…РѕРїР°РіР° / asyncpg РІ СЂР°РЅС‚Р°Р№РјС–
RUN apk add --no-cache libpq curl

# РЎС‚РІРѕСЂРµРЅРЅСЏ Р±РµР·РїРµС‡РЅРѕРіРѕ РєРѕСЂРёСЃС‚СѓРІР°С‡Р° (Non-root)
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# РљРѕРїС–СЋС”РјРѕ РїР°РєРµС‚Рё, СЃРєРѕРјРїС–Р»СЊРѕРІР°РЅС– РїС–Рґ musl-alpine
COPY --from=builder /root/.local /home/appuser/.local

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONPATH=/app

COPY --chown=appuser:appgroup ./app /app/app
COPY --chown=appuser:appgroup ./migrations /app/migrations
COPY --chown=appuser:appgroup ./alembic.ini /app/alembic.ini

USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT}/metrics || exit 1

EXPOSE ${PORT}

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
