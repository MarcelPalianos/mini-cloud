#!/bin/bash

echo "Pulling latest backend image..."
docker compose pull backend

echo "Recreating backend container..."
docker compose up -d --force-recreate backend

echo "Cleaning unused images..."
docker image prune -f

echo "Done."