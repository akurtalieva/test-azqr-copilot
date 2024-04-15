import json
import os

def load_paths():
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # Load paths from a JSON file
    with open(os.path.join(script_dir, 'settings.json'), 'r') as f:
        paths = json.load(f)

    # Add script_dir prefix to all paths
    for category in paths:
        for key in paths[category]:
            paths[category][key] = os.path.join(script_dir, paths[category][key])

    # Definition of the metadata file paths [INPUT]
    customers = paths['metadata']['customers']
    csv_path = paths['metadata']['csv_path']

    # Definition of the metadata file paths [OUTPUT]
    json_report = paths['metadata']['json_report']

    # Definition of the metaprompt file paths [PROCESSING]
    create_json = paths['metaprompt']['create_json']

    return customers, csv_path, json_report, create_json
