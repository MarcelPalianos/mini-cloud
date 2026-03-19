#!/bin/bash
set -e

echo "Pulling latest backend image..."
docker compose pull backend || { echo "Pull failed. Deployment stopped."; exit 1; }

echo "Recreating backend container..."
docker compose up -d --force-recreate backend

echo "Cleaning unused images..."
docker image prune -f

echo "Done."