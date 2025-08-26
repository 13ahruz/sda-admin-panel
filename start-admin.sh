#!/bin/bash

echo "Starting SDA Admin Panel with Docker Compose..."
echo

echo "Checking if .env file exists..."
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo
    echo "IMPORTANT: Please edit .env file with your database credentials!"
    echo
    read -p "Press enter to continue..."
fi

echo "Building and starting containers..."
docker-compose up --build

echo
echo "Admin Panel should be available at: http://localhost:8001/admin/"
echo "Default credentials: admin / admin123"
echo "IMPORTANT: Change the password after first login!"
