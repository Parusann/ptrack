# PTrack

PTrack is a multi-carrier shipment visibility platform. You give it tracking numbers from any carrier and it shows what is coming, when it will arrive, where each package is on a map, and whether it is likely to be late.

It is a small-scale version of the supply-chain "control tower" tools that construction and data-centre teams use to track long-lead parts, built first for tracking inbound inventory for a small resale business.

> Status: early development. See the roadmap below.

## Features (planned)

- **Carrier detection** from the tracking number alone, using format rules and check-digit validation
- **Direct carrier integrations** for FedEx, UPS, DHL and Canada Post, with an aggregator fallback for other carriers
- **Normalized milestones** so every carrier's statuses map to one shared model
- **Route map** of every scan event, geocoded and cached
- **Arrivals board and exceptions list** for planning: what lands today, what is stalled, what is held in customs
- **Delay prediction** that estimates how far off the carrier's promised date will be, with a calibrated range
- **Alerts** for out-for-delivery, delivered, exceptions and predicted delays

## Architecture

| Layer | Choice |
|---|---|
| Backend | FastAPI (Python 3.12), SQLAlchemy 2, Alembic |
| Frontend | React + TypeScript + Vite, MapLibre GL |
| Database | PostgreSQL (Neon) |
| Scheduled refresh | GitHub Actions |
| Hosting | Render (API), Cloudflare Pages (frontend) |
| ML | LightGBM quantile regression with conformal intervals |

Key design decisions are recorded in [`docs/adr/`](docs/adr/).

## Repository layout

```
backend/     FastAPI app, carrier adapters, jobs and tests
frontend/    React app (coming in phase 3)
docs/adr/    Architecture decision records
.github/     CI and scheduled workflows
```

## Getting started

Requirements: Python 3.12+

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp ../.env.example ../.env   # then fill in your own values
uvicorn ptrack.main:app --reload
```

The API runs at http://localhost:8000 and interactive docs are at http://localhost:8000/docs.

Run the tests:

```bash
cd backend
pytest
```

## Configuration

All credentials are read from environment variables. See [`.env.example`](.env.example) for the full list. Never commit a real `.env` file.

## Roadmap

1. Accounts and repo setup
2. Core: carrier detection, database schema, FedEx and DHL adapters
3. Route map and scheduled refresh
4. Control tower dashboard, business tags, alerts
5. Gmail import and carrier scorecard
6. Delay prediction and evaluation page
7. Polish and public demo
