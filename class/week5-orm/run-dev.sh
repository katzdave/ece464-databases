#!/usr/bin/env bash
set -e

# Start both server and client in parallel
trap 'kill 0' EXIT

echo "Starting server on :8095 ..."
(cd server && uv run uvicorn app.main:app --reload --port 8095) &

echo "Starting client on :3005 ..."
(cd client && npm run dev -- --port 3005) &

wait
