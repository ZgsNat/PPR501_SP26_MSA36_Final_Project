#!/bin/sh
set -e

# If the SQLite DB doesn't exist, run the seed script
if [ ! -f /app/students.db ]; then
  echo "students.db not found — running seed.py to initialize database"
  python seed.py
else
  echo "students.db found — skipping seeding"
fi

# Exec the passed command (uvicorn by default)
exec "$@"
