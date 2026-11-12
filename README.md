# Celtra DevOps Homework

A simple HTTP service that is tested, packaged in a Docker image and automatically deployed to production through a CI/CD pipeline on every push to `main`.

The specification is in [SPEC.md](SPEC.md).

Live app available on: https://celtra-homework-0d0b6b4c5457.herokuapp.com/demo/data

Example of data returned:
```json
{
  "accountId": "demo",
  "timestamp": "2026-11-11T15:47:51Z",
  "data": "cd1d6bea-3e50-40a2-8c98-aefb32f5ac48"
}
```

Replace `demo` with any account ID.



## Stack

| Part | Tool |
|---|---|
| Service | Python 3.13, Flask, gunicorn |
| Tests | pytest |
| Container | Docker (`test` and `runtime` images) |
| CI/CD | GitHub Actions |
| Hosting | Heroku (container stack, one Basic dyno) |
| Monitoring | Grafana Cloud Synthetic Monitoring |

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

python -m app.main            # serves on http://localhost:8000
python -m pytest -v           # runs the unit tests
```

Then open <http://localhost:8000/demo/data>.

## Run with Docker

```bash
# Unit tests inside the test image
docker build --target test -t app:test .
docker run --rm app:test

# Production image
docker build --target runtime -t app:runtime .
docker run --rm -p 8000:8000 app:runtime
```
