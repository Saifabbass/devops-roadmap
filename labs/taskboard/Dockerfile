# Digests verified from Docker Hub's registry API on 2026-10-20.
ARG PYTHON_IMAGE=python:3.14-slim-bookworm@sha256:48b13b003dda20b16f9442b8475aa05fe21bf6579a8c881db92ffb4d8fd20f83
FROM ${PYTHON_IMAGE} AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.lock ./
RUN python -m pip install --no-cache-dir -r requirements.lock     && groupadd --gid 10001 taskboard     && useradd --uid 10001 --gid 10001 --no-create-home taskboard
COPY reference ./reference
COPY migrations ./migrations
ARG GIT_SHA=development
ENV GIT_SHA=${GIT_SHA}
USER 10001:10001
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "reference.stage07:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]

FROM runtime AS tests
USER root
COPY requirements-dev.lock ./
RUN python -m pip install --no-cache-dir -r requirements-dev.lock
COPY tests ./tests
COPY tools ./tools
COPY pytest.ini ./
USER 10001:10001
CMD ["python", "-m", "pytest", "tests/unit", "tests/contract", "-p", "no:cacheprovider"]
