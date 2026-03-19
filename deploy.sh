#!/bin/bash

echo "Pulling latest backend image..."
docker compose pull backend

echo "Updating containers..."
docker compose up -d

echo "Cleaning unused images..."
docker image prune -f

echo "Done."