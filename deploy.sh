#!/bin/bash
set -e

echo "Pulling latest backend image..."
for i in 1 2 3; do
  if docker compose pull backend; then
    break
  fi
  echo "Pull failed, retrying in 5 seconds... ($i/3)"
  sleep 5
done

echo "Getting latest commit SHA..."
export COMMIT_SHA=$(git rev-parse --short HEAD)

echo "Recreating backend container..."
docker compose up -d --force-recreate backend

echo "Recreating web"
docker compose up -d --force-recreate backend web

echo "Cleaning unused images..."
docker image prune -f

echo "Done. Running commit: $COMMIT_SHA"