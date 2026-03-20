import json

# --- Configuration ---
# The path to your JSON file
json_path = "C:\\CPU2BP\\CSR\\save\\measurement_catalog.json"
# The specific 'name' you want to target for the update
target_name = "MMC_CPD_FP_20260225"
# --- End of Configuration ---


def update_entry(entry_data):
    """
    Updates the 'files' list to a dictionary for a given JSON object.
    Returns True if an update was made, False otherwise.
    """
    update_made = False
    if 'folders' in entry_data and isinstance(entry_data['folders'], list):
        for folder in entry_data['folders']:
            if 'files' in folder and isinstance(folder['files'], list):
                files_list = folder['files']
                # Convert the list to a dictionary with null values
                files_dict = {filename: None for filename in files_list}
                folder['files'] = files_dict
                update_made = True
    return update_made

try:
    # Open and read the JSON file
    with open(json_path, 'r') as f:
        data = json.load(f)

    entry_found = False
    update_performed = False

    # Scenario 1: The file contains a list of entries
    if isinstance(data, list):
        print("File contains a list. Searching for the target entry...")
        for entry in data:
            if isinstance(entry, dict) and entry.get('name') == target_name:
                entry_found = True
                print(f"Found entry: '{target_name}'.")
                if update_entry(entry):
                    update_performed = True
                break  # Stop after finding the first match

    # Scenario 2: The file contains a single entry
    elif isinstance(data, dict):
        print("File contains a single entry. Checking if it's the target...")
        if data.get('name') == target_name:
            entry_found = True
            print(f"Entry is the target: '{target_name}'.")
            if update_entry(data):
                update_performed = True

    # --- Finalizing and Saving ---
    if not entry_found:
        print(f"\nResult: No entry with the name '{target_name}' was found. The file remains unchanged.")
    elif not update_performed:
        print(f"\nResult: Entry '{target_name}' was found, but no changes were needed. The 'files' key may already be in the correct format or is missing.")
    else:
        # Write the updated data back to the file only if a change was made
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"\nSuccess! The entry '{target_name}' was updated in {json_path}")

except FileNotFoundError:
    print(f"Error: The file at {json_path} was not found.")
except json.JSONDecodeError:
    print(f"Error: The file at {json_path} is not a valid JSON file.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

