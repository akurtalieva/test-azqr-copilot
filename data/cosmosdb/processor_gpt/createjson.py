#!/usr/bin/env python3

import glob
import subprocess
import os
import time
import json
import settings

def main():
    customers, csv_path, azqr_report_cost, azqr_report_advisor, azqr_report_defender, azqr_report_services, json_report, create_json = settings.load_paths()

    # Obtiene una lista de todos los archivos .csv en el directorio
    csv_files = glob.glob(csv_path)

    global_start_time = time.time()

    if os.path.isfile(json_report):
        overwrite = input(f"El archivo {json_report} ya existe. ¿Desea sobrescribirlo? (s/n): ")
        if overwrite.lower() != 's':
            print("Saliendo sin sobrescribir el archivo.")
            return    

    start_time = time.time()
    print("Creating JSON file...", end="")
    subprocess.run(["python", "data/cosmosdb/processor/gpt4.py", "--max_tokens" , "4080" , "--files", create_json , customers, *csv_files], stdout=open(json_report, "w"))
    print(f"done! {time.time() - start_time} seconds")

    elapsed_time = time.time() - global_start_time
    minutes = int(elapsed_time / 60)
    seconds = int(elapsed_time % 60)
    print(f"Process completed in: {minutes} minutes {seconds} seconds")
    
if __name__ == "__main__":
    main()