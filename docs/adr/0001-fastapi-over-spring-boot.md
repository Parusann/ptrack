# ADR 0001: FastAPI over Spring Boot for the backend

- Status: Accepted
- Date: 2026-09-26

## Context

PTrack runs on a strict $0 budget. The only forever-free container host that needs no credit card is Render's free web service: 512 MB of RAM, a fraction of one CPU, and it sleeps after 15 minutes without traffic.

The backend also has to serve a delay-prediction model trained with LightGBM and scikit-learn.

## Decision

Use FastAPI (Python 3.12) with SQLAlchemy 2 and Alembic.

## Reasons

- The JVM alone takes a large share of 512 MB, and Spring Boot cold starts on a fractional CPU are slow. Out-of-memory crashes on that tier are a real risk.
- The ML model is trained in Python and can be served directly, with no ONNX conversion or native Java bindings.
- One language across the API, the scheduled refresh job and the ML pipeline keeps the project simpler.

## Consequences

- Spring Boot experience is not showcased here. If the project moves to a larger host, a Java service could be revisited.
- Memory use should be measured with `docker stats` and kept well under 512 MB.
