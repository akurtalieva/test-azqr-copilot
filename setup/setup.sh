#!/bin/bash

set -e

resourceGroupLocation="swedencentral"
resourceGroupName="test-azqr-rg"
deploymentName="azqr-deployment"
scriptDir=$(dirname "$(realpath "$0")")


function login {
    # Load environment variables from .env file
    if [ -f "$scriptDir/../.env" ]; then
        source "$scriptDir/../.env"
    fi

    if [ -z "$TENANT_ID" ]; then
        echo "TENANT_ID is not set. Please check your .env file."
        exit 1
    fi

    if [ -z "$SUBSCRIPTION_ID" ]; then
        echo "SUBSCRIPTION_ID is not set. Please check your .env file."
        exit 1
    fi

    az login --use-device-code -t $TENANT_ID
    az account set --subscription $SUBSCRIPTION_ID
}

function check_login {
    if [ -z "$(az account show)" ]; then
        echo "You are not logged in. Please run 'az login' or 'az login --use-device-code --tenant XXXXX' first."
        exit 1
    fi
}

function create_resource_group {
    echo "Creating resource group $resourceGroupName in $resourceGroupLocation..."
    az group create --name $resourceGroupName --location $resourceGroupLocation > /dev/null
}

function provision_resources {
    echo "Provisioning resources in resource group $resourceGroupName..."
    #az deployment group create --resource-group $resourceGroupName --name $deploymentName --only-show-errors --template-file main.bicep > /dev/null
    az deployment group create --resource-group $resourceGroupName --name $deploymentName --template-file main.bicep 
}

function setup_environment_variables {
    echo "Setting up environment variables in .env file..."
    # Save output values to variables
    openAiService=$(az deployment group show --name $deploymentName --resource-group $resourceGroupName --query properties.outputs.openai_name.value -o tsv)
    searchService=$(az deployment group show --name $deploymentName --resource-group $resourceGroupName --query properties.outputs.search_name.value -o tsv)
    cosmosService=$(az deployment group show --name $deploymentName --resource-group $resourceGroupName --query properties.outputs.cosmos_name.value -o tsv)
    searchEndpoint=$(az deployment group show --name $deploymentName --resource-group $resourceGroupName --query properties.outputs.search_endpoint.value -o tsv)
    openAiEndpoint=$(az deployment group show --name $deploymentName --resource-group $resourceGroupName --query properties.outputs.openai_endpoint.value -o tsv)
    cosmosEndpoint=$(az deployment group show --name $deploymentName --resource-group $resourceGroupName --query properties.outputs.cosmos_endpoint.value -o tsv)
    mlProjectName=$(az deployment group show --name $deploymentName --resource-group $resourceGroupName --query properties.outputs.mlproject_name.value -o tsv)

    # Get keys from services
    searchKey=$(az search admin-key show --service-name $searchService --resource-group $resourceGroupName --query primaryKey --output tsv)
    apiKey=$(az cognitiveservices account keys list --name $openAiService --resource-group $resourceGroupName --query key1 --output tsv)
    cosmosKey=$(az cosmosdb keys list --name $cosmosService --resource-group $resourceGroupName --query primaryMasterKey --output tsv)

    # Write environment variables to .env file
    echo "# AZURE AI SERVICES  " >> ../.env
    echo "AZURE_AI_SERVICES_ENDPOINT=$openAiEndpoint" >> ../.env
    echo "AZURE_AI_SERVICES_KEY=$apiKey" >> ../.env
    echo "AZURE_AI_SERVICES_VERSION=2024-03-01-preview" >> ../.env
    echo "AZURE_AI_GPT_DEPLOYMENT=gpt-4-1106-preview" >> ../.env
    echo "AZURE_AI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002" >> ../.env      
    echo " " >> ../.env
    echo "# AZURE COSMOS  " >> ../.env 
    echo "COSMOS_ENDPOINT=$cosmosEndpoint" >> ../.env
    echo "COSMOS_KEY=$cosmosKey" >> ../.env
    echo " " >> ../.env
    echo "# AZURE SEARCH" >> ../.env
    echo "AZURE_SEARCH_ENDPOINT=$searchEndpoint" >> ../.env
    echo "AZURE_SEARCH_KEY=$searchKey" >> ../.env
    echo "AZURE_SEARCH_INDEX_NAME=azure-well-architected" >> ../.env
    
}

function write_config_json {
    echo "Writing config.json file for PromptFlow usage..."
    subscriptionId=$(az account show --query id -o tsv)
    echo "{\"subscription_id\": \"$subscriptionId\", \"resource_group\": \"$resourceGroupName\", \"workspace_name\": \"$mlProjectName\"}" > ../config.json
}

login
check_login
create_resource_group
provision_resources
setup_environment_variables
write_config_json

echo "Provisioning complete!"