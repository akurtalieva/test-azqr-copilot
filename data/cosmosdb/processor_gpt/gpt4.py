#!/usr/bin/env python3

import os
import sys
import argparse
import azureoai
from openai import AzureOpenAI
from dotenv import load_dotenv

def get_completion_files(client, prompt, max_tokens):
    messages = [{"role": "system", "content": prompt},
                {"role": "user", "content": ""}] 
    try:
        response = client.chat.completions.create(   
            model=os.getenv('AZURE_OPENAI_DEPLOYMENT'),                                         
            messages=messages,
            temperature=0.7,
            max_tokens=max_tokens,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_completion(client, prompt, max_tokens):
    messages = [{"role": "user", "content": prompt}] 
    try:
        response = client.chat.completions.create(   
            model=os.getenv('AZURE_OPENAI_DEPLOYMENT'),                                         
            messages=messages,
            temperature=0.7,
            max_tokens=max_tokens,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return None

def main(text=None, filenames=None, max_tokens=2000):
    client = azureoai.setup_client()

    if filenames:
        text = ""
        for filename in filenames:
            with open(filename, 'r') as file:
                text += file.read()

        prompt = f"""
            {text}
        """
        response = get_completion_files(client, prompt, max_tokens)        
    else:       
        prompt = f"""
            {text}
        """
        response = get_completion(client, prompt, max_tokens)

    if response:
        print(response)

def load_variables():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    path=os.path.join(os.curdir, script_dir + "/../../../.env")
    load_dotenv(path)

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description='Genera una respuesta con IA Generativa.')    
    parser.add_argument('--prompt', "-p", type=str, 
                        help='El texto a partir del cual se generará la respuesta.')
    parser.add_argument('--files', "-f", nargs='+', type=str, 
                        help='Los nombres de los archivos que contienen el texto a partir del cual se generará la respuesta.')
    parser.add_argument('--max_tokens', "-m", type=int, 
                        help='El número máximo de tokens que se generarán.')
    
    args = parser.parse_args()

    load_variables()
    
    #args.prompt = f"En un contexto de AI Generativa, ¿que significa el termino 'data grounding'?"
    main(args.prompt, args.files, args.max_tokens)