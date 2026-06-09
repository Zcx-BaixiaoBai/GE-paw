# Stage 1: build web console (vite)
FROM node:20-alpine AS web-builder
WORKDIR /build
COPY web/package.json web/pnpm-lock.yaml* web/package-lock.json* ./
RUN if [ -f pnpm-lock.yaml ]; then corepack enable && pnpm install --frozen-lockfile; elif [ -f package-lock.json ]; then npm ci; else npm install; fi
COPY web/ ./
RUN npm run build

# Stage 2: runtime (Python + FastAPI)
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends build-essential libffi-dev libssl-dev && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml setup.py README.md ./
COPY src ./src
RUN pip install --no-cache-dir -e .

COPY --from=web-builder /build/dist ./web/dist

EXPOSE 8765
CMD ["python", "-m", "gepaw", "serve", "--host", "0.0.0.0", "--port", "8765"]
