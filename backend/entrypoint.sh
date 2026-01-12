#!/bin/sh
set -e

# File DB sqlite sẽ được tạo ở /app/students.db
if [ ! -f /app/students.db ]; then
  echo "students.db not found — running dirty_seed.py..."
  # Chạy dirty_seed.py
  python dirty_seed.py
else
  echo "students.db found — skipping seeding"
fi

# Chạy lệnh CMD (uvicorn)
exec "$@"