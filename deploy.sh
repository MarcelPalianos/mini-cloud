#!/bin/bash

echo "Pulling latest code..."
git pull

echo "Rebuilding containers..."
docker compose build

echo "Restarting services..."
docker compose up -d

echo "Cleaning unused images..."
docker image prune -f

echo "Done."