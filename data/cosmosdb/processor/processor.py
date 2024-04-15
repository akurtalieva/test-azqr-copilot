import csv
import json
import glob
import settings

# Function to read CSV files and return a list of dictionaries
def read_csv_data(file_name):
    data = []
    with open(file_name, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            data.append(row)
    return data

# Function to match subscription and append the data to the corresponding customer
def append_data_to_customer(customer, data, key):
    customer[key] = [item for item in data if item['Subscription'] == customer['Subscription']]

def main():
    customers, csv_path, json_report, create_json = settings.load_paths()

    # Read customers.json and store data
    with open(customers, 'r') as json_file:
        customers_data = json.load(json_file)

    # Read CSV files
    csv_files = glob.glob(csv_path)

    # Rename the 'Subscription' key to 'Subscription' and 'TenantID' key to 'Tenant'
    for customer in customers_data['customers']:
        customer['Subscription'] = customer.pop('Subscription')
        customer['Tenant'] = customer.pop('Tenant')
    
    # Add CSV data to customers_data under the corresponding keys
    for customer in customers_data['customers']:
        for csv_file in csv_files:
            data = read_csv_data(csv_file)
            file_name = csv_file.rsplit('.', 2)[-2]
            append_data_to_customer(customer, data, file_name)

    # Write the final JSON structure to a file
    with open(json_report, 'w') as outfile:
        json.dump(customers_data, outfile, indent=4)

if __name__ == "__main__":
    main()