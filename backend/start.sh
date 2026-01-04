#!/bin/bash
alembic upgrade head
python seed_tvet_schools.py
uvicorn app.main:app --host 0.0.0.0 --port $PORT
