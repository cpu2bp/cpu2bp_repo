import pandas as pd
import json
import numpy as np

# Define the paths for the Excel and JSON files
excel_path = r'C:\CPU2BP\CSR\MMC\CPD_measurement_catalogue (1).xlsx'
json_path = r'c:\CPU2BP\CSR\MMC\newjson_02.json'

# Define the ground truth dictionary that will be used for new entries
gt_block = {
    "CPD_GT": "empty",
    "OC_Adult_GT": 0,
    "OC_GT": 0,
    "SOD_GT": {
        "1L": "E", "1R": "C",
        "2L": "E", "2M": "E", "2R": "E",
        "3L": "E", "3R": "E"
    },
    "M_BLD_GT": 0,
    "S_BLD_GT": 0,
    "M_INTERFERENCE_GT": 0,
    "S_INTERFERENCE_GT": 0
}

# Read the JSON file
with open(json_path, 'r') as f:
    json_data = json.load(f)

# Read the Excel file
df = pd.read_excel(excel_path)

# Filter the DataFrame to only include relevant rows
relevant_df = df[df['Relevant for resim [Y/N]'] == 'Y'].copy()

# Get a set of all existing measurement names in the JSON for quick lookup
existing_measurements = set()
for folder in json_data[1]['folders']:
    if 'files' in folder:
        for file_name in folder['files']:
            existing_measurements.add(file_name)

# Create a mapping from the top-level "name" to the corresponding object in the JSON data
target_map = {item.get('name'): item for item in json_data if 'name' in item}

# Iterate over the relevant rows in the DataFrame
for index, row in relevant_df.iterrows():
    measurement_name = row['Measurement name']
    
    # If the measurement name is not already in the JSON, process it
    if measurement_name not in existing_measurements:
        target_measurement_set = row['TargetMeasurementSet']
        location = row['Location']
        json_comment = row['JsonComment']

        # Check if the target_measurement_set exists in the JSON data
        if target_measurement_set in target_map:
            target_object = target_map[target_measurement_set]
            
            # Find if a folder with the same root already exists
            existing_folder = None
            for folder in target_object.get('folders', []):
                if folder.get('root') == location:
                    existing_folder = folder
                    break
            
            file_entry = None
            if pd.isna(json_comment):
                file_entry = None
            else:
                file_entry = json_comment

            if existing_folder is not None:
                # Add the file to the existing folder
                existing_folder.setdefault('files', {})[measurement_name] = file_entry
            else:
                # Create a new folder entry if root does not exist
                new_folder = {
                    "root": location,
                    "files": {measurement_name: file_entry},
                    "gt": gt_block
                }
                target_object.setdefault('folders', []).append(new_folder)
        else:
            # If the target_measurement_set does not exist, create a new one.
            file_entry = None
            if pd.isna(json_comment):
                file_entry = None
            else:
                file_entry = json_comment
            
            new_target_object = {
                "name": target_measurement_set,
                "folders": [
                    {
                        "root": location,
                        "files": {
                            measurement_name: file_entry
                        },
                        "gt": gt_block
                    }
                ],
                "simulation_mode": "asw_resim"
            }
            json_data.append(new_target_object)
            # Add the new object to the map for subsequent iterations
            target_map[target_measurement_set] = new_target_object

# Write the updated JSON data back to the file
with open(json_path, 'w') as f:
    json.dump(json_data, f, indent=4)

print("JSON file has been updated successfully.")
