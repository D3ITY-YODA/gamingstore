#!/bin/bash

# Generate unique app name
APP_NAME="brendangamingstore$(date +%s)"
echo "🚀 Deploying to: $APP_NAME"

# Create resource group first
echo "Creating resource group..."
az group create \
    --name gamingstore-rg \
    --location eastus

# Create storage account for media
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
echo "📝 Note: You'll need to configure deployment separately"
