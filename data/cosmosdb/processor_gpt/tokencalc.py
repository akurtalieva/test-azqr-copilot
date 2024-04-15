import tiktoken
import os
import settings
import glob

def num_tokens_from_string(string: str, model: str) -> int:
    """Returns the number of tokens in a text string."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    num_tokens = len(encoding.encode(string))
    return num_tokens

def main():
    customers, csv_path, json_report, create_json = settings.load_paths()

    # Obtiene una lista de todos los archivos .csv en el directorio
    csv_files = glob.glob(csv_path)

    total_tokens = 0

    for csv_file in csv_files:
        with open(csv_file, 'r') as file:
            texto = file.read().replace('\n', ' ')

            # Obtiene el nombre del archivo 
            file_name_parts = os.path.basename(csv_file).rsplit('.', 2)
            name = file_name_parts[-2] if len(file_name_parts) > 1 else ''

            # Calcula el número de tokens en el archivo
            num_tokens = num_tokens_from_string(texto, "gpt-4-1106-preview")

            # Imprime el número de tokens en el archivo
            print("Número de tokens en", name, ": ", num_tokens)

            # Suma el número de tokens al total
            total_tokens += num_tokens

    # Imprime el total de tokens
    print("Total de tokens: ", total_tokens)

if __name__ == "__main__":
    main()