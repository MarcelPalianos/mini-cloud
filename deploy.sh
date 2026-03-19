#!/bin/bash
set -e

echo "Pulling latest backend image..."
docker compose pull backend

echo "Getting latest commit SHA..."
export COMMIT_SHA=$(git rev-parse --short HEAD)

echo "Recreating backend container..."
docker compose up -d --force-recreate backend

echo "Cleaning unused images..."
docker image prune -f

echo "Done. Running commit: $COMMIT_SHA"