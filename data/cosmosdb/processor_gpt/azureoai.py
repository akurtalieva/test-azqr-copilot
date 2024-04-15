import os
import sys
from openai import AzureOpenAI

def setup_client():
    api_version = os.getenv("AZURE_OPENAI_VERSION")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')    

    if not api_version or not api_key or not azure_endpoint:
        print("Error: Las variables de entorno AZURE_OPENAI_VER, AZURE_OPENAI_KEY y AZURE_OPENAI_ENDPOINT no están definidas.")
        sys.exit(1)

    return AzureOpenAI(
        api_version=api_version,
        api_key=api_key,  
        azure_endpoint=azure_endpoint
    )
