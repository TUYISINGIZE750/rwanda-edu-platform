#!/bin/bash
python check_db.py
python seed_simple.py
uvicorn app.main:app --host 0.0.0.0 --port $PORT
