import json

# --- Configuration ---
# The path to your JSON file
file_path = "C:\\CPU2BP\\CSR\\MMC\\newjson_Outside_modified.json"

# --- End of Configuration ---

print(f"Starting advanced formatting for: {file_path}")

try:
    with open(file_path, 'r') as f:
        data = json.load(f)
    print("--> Successfully loaded JSON file.")

    # A list to hold the original data from each SOD_GT section we find
    stored_sod_gt_data = []
    # A counter to create a unique placeholder for each section
    placeholder_index = 0

    # Step 1: Find all entries and replace all SOD_GT sections with unique placeholders
    if isinstance(data, list):
        for entry in data:
            if isinstance(entry, dict):
                print(f"--> Processing entry: '{entry.get('name', 'N/A')}'. Storing original SOD_GT data...")
                for folder in entry.get('folders', []):
                    if 'gt' in folder and 'SOD_GT' in folder.get('gt', {}):
                        # Store the original data
                        stored_sod_gt_data.append(folder['gt']['SOD_GT'])
                        # Create and set a unique placeholder
                        placeholder_string = f"___SOD_GT_PLACEHOLDER_{placeholder_index}___"
                        folder['gt']['SOD_GT'] = placeholder_string
                        placeholder_index += 1
    
    if not stored_sod_gt_data:
        raise ValueError("No 'SOD_GT' sections were found in the entire file to format.")

    print(f"--> Found and stored {len(stored_sod_gt_data)} SOD_GT section(s).")

    # Step 2: Convert the data structure (with placeholders) to a pretty-printed string
    json_with_placeholders = json.dumps(data, indent=4)

    final_content = json_with_placeholders
    key_indent = " " * 16  # Indentation of the "SOD_GT" key
    value_indent = " " * 20 # Indentation of the value lines

    # Step 3: Loop through the stored data and replace each placeholder
    print("--> Dynamically creating formatted blocks and replacing placeholders...")
    for i, original_data in enumerate(stored_sod_gt_data):
        # Dynamically build the custom formatted block using the original data
        custom_formatted_block = f'''{key_indent}"SOD_GT": {{
{value_indent}"1L" : "{original_data.get('1L', 'E')}",             "1R" : "{original_data.get('1R', 'E')}",
{value_indent}"2L" : "{original_data.get('2L', 'E')}", "2M" : "{original_data.get('2M', 'E')}", "2R" : "{original_data.get('2R', 'E')}",
{value_indent}"3L" : "{original_data.get('3L', 'E')}",             "3R" : "{original_data.get('3R', 'E')}"
{key_indent}}}'''

        # The placeholder line that json.dumps would have created
        placeholder_line = f'{key_indent}"SOD_GT": "___SOD_GT_PLACEHOLDER_{i}___"'
        
        # Replace the placeholder line with our dynamically created block
        final_content = final_content.replace(placeholder_line, custom_formatted_block)

    # Step 4: Write the final, fully corrected content back to the file
    with open(file_path, 'w') as f:
        f.write(final_content)

    print(f"\nResult: SUCCESS! The file has been updated with custom formatting while preserving original data.")

except FileNotFoundError:
    print(f"Error: The file at {file_path} was not found.")
except (ValueError, Exception) as e:
    print(f"An error occurred: {e}")

