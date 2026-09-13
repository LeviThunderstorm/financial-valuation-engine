
# Real-Time Financial Valuation & Equity Analytics Engine

![CI/CD Pipeline](https://github.com/<your-github-username>/finance-analytics-engine/actions/workflows/deploy.yml/badge.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/<your-dockerhub-username>/finance-backend?color=blue&label=Docker%20Hub)
![License](https://img.shields.io/badge/license-MIT-green)

A production-grade, 3-tier microservice platform for real-time equity analytics and Discounted Cash Flow (DCF) valuation logging. Designed with modern DevOps practices featuring multi-stage Docker containerization, dynamic reverse proxying via Nginx, persistent relational data management, and an automated GitHub Actions CI/CD pipeline building to Docker Hub.

---

## ── Architecture Overview


                      [ Developer Workstation ]
                                 │
                       ( git push origin main )
                                 │
                                 ▼
                        [ GitHub Actions ]
                                 │
             ┌───────────────────┴───────────────────┐
             ▼                                       ▼
    [ Job 1: Test & Lint ]               [ Job 2: Build & Push ]
    ├── PostgreSQL Service               ├── Multi-Stage Docker Builds
    └── Health Check Verification        └── Push to Docker Hub
                                                     │
                                                     ▼
                                           [ Docker Hub Registry ]
                                           ├── finance-backend:latest
                                           └── finance-frontend:latest




```

```
                    [ Production Container Stack ]
                                 │

```

┌───────────────────────────────────┼───────────────────────────────────┐
│                                   ▼                                   │
│                        [ Nginx Reverse Proxy ]                        │
│                               (Port 80)                               │
│                                   │                                   │
│                 ┌─────────────────┴─────────────────┐                 │
│                 ▼                                   ▼                 │
│       [ Frontend Dashboard ]               [ Backend API ]            │
│           (Static HTML/JS)                 (FastAPI/Uvicorn)          │
│                                                     │                 │
│                                                     ▼                 │
│                                           [ PostgreSQL Database ]     │
│                                           (Volume Persistence)        │
└───────────────────────────────────────────────────────────────────────┘

```

---

## ── Key Features & Tech Stack

### Financial Analytics Features
* **5-Year DCF Valuation Model:** Computes intrinsic equity values using discounted projected free cash flows and Gordon Growth terminal values.
* **Valuation Logging & Tracking:** Logs real-time ticker calculations to PostgreSQL to maintain execution history and market delta classifications (`UNDERVALUED`, `OVERVALUED`, `FAIRLY VALUED`).

### Core Technology Stack
* **Backend:** Python 3.11, FastAPI, SQLAlchemy, Uvicorn.
* **Frontend:** HTML5, JavaScript (ES6+), CSS3.
* **Reverse Proxy:** Nginx (Alpine Linux).
* **Database:** PostgreSQL 15 with Docker named volumes for state persistence.
* **DevOps & CI/CD:** Docker, Docker Compose, Git, GitHub Actions, Docker Hub.

---

## ── DevOps & CI/CD Pipeline Design

### 1. Multi-Stage Containerization
Both application tiers utilize multi-stage `Dockerfile` definitions to reduce image footprint and enforce security:
* **Backend:** Builder stage compiles C-extensions (`libpq-dev`), passing pre-built wheel dependencies to a minimal `python:3.11-slim` runtime running under an unprivileged non-root user (`appuser`).
* **Frontend:** Builder stage compiles static web assets, serving them via an unprivileged `nginx:1.25-alpine` runtime with custom location routing to eliminate Cross-Origin Resource Sharing (CORS) friction.

### 2. Dual-Environment Orchestration
* **Local Development (`docker-compose.yml`):** Utilizes bind mounts for live hot-reloading (`uvicorn --reload`) and exposes direct port bindings for rapid debugging.
* **Production Deployment (`docker-compose.prod.yml`):** Pulls immutable, pre-compiled images directly from Docker Hub, using network isolation and non-volatile database volumes.

### 3. Automated CI/CD Workflow (`.github/workflows/deploy.yml`)
* **Job 1 (Test & Validation):** Launches an ephemeral PostgreSQL container service inside the GitHub runner to perform automated schema initialization and package health checks.
* **Job 2 (Build & Publish):** Authenticates securely to Docker Hub using GitHub Secrets, builds multi-stage Docker images using `docker/build-push-action` with layer caching (`gha`), and tags outputs using both the `git commit SHA` and `latest`.
* **Job 3 (Production Deployment):** Executes automated deployment triggers via SSH to update production runtime environments.

---

## ── Quick Start & Local Execution

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed locally.
* [Git](https://git-scm.com/) installed.

### 1. Clone the Repository
```bash
git clone https://github.com/LeviThunderstorm/financial-valuation-engine
cd finance-analytics-engine

```

### 2. Run Local Development Stack

```bash
# Start all microservices in hot-reloading mode
docker compose up --build

```

Access the application dashboard at `http://localhost`.

### 3. Run Production Stack using Docker Hub Images

```bash
# Pull and launch pre-built production images from Docker Hub
DOCKERHUB_USERNAME="levithunderstorm" docker compose -f docker-compose.prod.yml up -d

```

---

## ── API Documentation

The backend service automatically generates interactive OpenAPI/Swagger documentation.

* **Swagger UI:** `http://localhost:8000/docs`
* **Health Check Endpoint:** `GET /health`
* **DCF Valuation Endpoint:** `POST /api/v1/valuation/dcf`
* **Valuation History Endpoint:** `GET /api/v1/valuation/history`

---

## ── Author

**Levi Thunderstorm**  
*Cybersecurity Analyst, DevOps Engineer & Finance Analyst*  
* **GitHub:** [@LeviThunderstorm](https://github.com/LeviThunderstorm)
```

```