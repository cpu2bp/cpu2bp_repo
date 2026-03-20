import openpyxl
import json

def create_json_from_excel(excel_path, json_path):
    """
    Reads an Excel file and generates a JSON file with a specific nested structure.

    Args:
        excel_path (str): The path to the input Excel file.
        json_path (str): The path to the output JSON file.
    """
    try:
        workbook = openpyxl.load_workbook(excel_path)
        sheet = workbook.active
    except FileNotFoundError:
        print(f"Error: Excel file not found at {excel_path}")
        return

    header = [cell.value for cell in sheet[1]]
    try:
        target_set_col = header.index("TargetMeasurementSet")
        location_col = header.index("Location")
        measurement_name_col = header.index("Measurement name")
        json_comment_col = header.index("JsonComment")
    except ValueError as e:
        print(f"Error: A required column was not found in the Excel file - {e}")
        print(f"Available columns are: {header}")
        return

    data = {}
    for row in sheet.iter_rows(min_row=2, values_only=True):
        target_set = row[target_set_col]
        location = row[location_col]
        measurement_name = row[measurement_name_col]
        json_comment = row[json_comment_col]

        if not target_set or not location or not measurement_name:
            continue

        if target_set not in data:
            data[target_set] = {
                "name": target_set,
                "folders": [],
                "simulation_mode": "asw_resim" # Default value
            }

        # Find or create the folder for the current location
        folder = next((f for f in data[target_set]["folders"] if f["root"] == location), None)
        if folder is None:
            folder = {
                "root": location,
                "files": {},
                "gt": {
                    "CPD_GT": "empty",
                    "OC_Adult_GT": 0,
                    "OC_GT": 0,
                    "SOD_GT": {
                        "1L": "E", "1R": "X",
                        "2L": "E", "2M": "E", "2R": "X",
                        "3L": "E", "3R": "X"
                    },
                    "M_BLD_GT": 0,
                    "S_BLD_GT": 0,
                    "M_INTERFERENCE_GT": 0,
                    "S_INTERFERENCE_GT": 0
                }
            }
            data[target_set]["folders"].append(folder)

        folder["files"][measurement_name] = json_comment if json_comment else None

    # Convert the dictionary of measurement sets to a list
    output_data = list(data.values())

    try:
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
        print(f"Successfully created JSON file at {json_path}")
    except IOError as e:
        print(f"Error writing to JSON file: {e}")

if __name__ == "__main__":
    excel_file = r"C:\CPU2BP\CSR\MMC\CPD_measurement_catalogue.xlsx"
    json_file = r"C:\CPU2BP\CSR\MMC\newjson.json"
    create_json_from_excel(excel_file, json_file)
