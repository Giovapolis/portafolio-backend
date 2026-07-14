#!/bin/bash
set -e

echo "Waiting for database..."
for i in $(seq 1 30); do
  if alembic upgrade head 2>/dev/null; then
    echo "Migrations applied successfully"
    break
  fi
  if [ "$i" -eq 30 ]; then
    echo "ERROR: Database not reachable after 30 attempts"
    exit 1
  fi
  echo "  attempt $i/30 - database not ready, retrying in 2s..."
  sleep 2
done

echo "Seeding admin user..."
python -m app.db.init_db

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
