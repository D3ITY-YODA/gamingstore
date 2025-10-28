#!/bin/bash
set -e

# Set your unique app name
APP_NAME="brendangamingstore$(date +%s)"
echo "🚀 Deploying to: $APP_NAME"

# Create resource group
echo "Creating resource group..."
az group create --name gamingstore-rg --location "eastus"

# Create PostgreSQL database
echo "Creating PostgreSQL database..."
az postgres flexible-server create \
    --resource-group gamingstore-rg \
    --name gamingstore-db \
    --location eastus \
    --admin-user djangoadmin \
    --admin-password "SecurePassword123!" \
    --sku-name Standard_B1ms \
    --tier Burstable \
    --storage-size 32 \
    --version 13

# Create storage account
echo "Creating storage account..."
az storage account create \
    --name "gamingstoremedia$(date +%s)" \
    --resource-group gamingstore-rg \
    --location eastus \
    --sku Standard_LRS

# Create app service plan
echo "Creating app service plan..."
az appservice plan create \
    --name gamingstore-plan \
    --resource-group gamingstore-rg \
    --sku F1 \
    --is-linux

# Create web app
echo "Creating web app..."
az webapp create \
    --resource-group gamingstore-rg \
    --plan gamingstore-plan \
    --name "$APP_NAME" \
    --runtime "PYTHON:3.11"

echo "✅ Azure resources created! App name: $APP_NAME"
