# Multi-stage build:
#   base    -> Python + runtime dependencies + app code
#   test    -> base + pytest + tests (used only in CI)
#   runtime -> base + non-root user, started with gunicorn (deployed to production)
# Both test and runtime start from the same base, so the tests run
# against exactly the same app code and dependencies that ship to production.

FROM python:3.13-slim AS base

# Don't write .pyc files; send logs straight to stdout (visible in Heroku logs)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first, so this layer is cached when only code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/


FROM base AS test

COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY tests/ tests/

CMD ["python", "-m", "pytest", "-v"]


FROM base AS runtime

# Run as a non-root user
RUN useradd --create-home appuser
USER appuser

# Heroku sets $PORT at runtime; 8000 is the default for running locally.
# "sh -c" is needed so ${PORT} is expanded; exec makes gunicorn PID 1,
# so it receives stop signals directly and shuts down cleanly.
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT:-8000} --workers 2 --access-logfile - app.main:app"]