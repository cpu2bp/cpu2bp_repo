import csv
import json
import os
import re
from collections import defaultdict

csv_path = r'c:\\Users\\cpu2bp\\Downloads\\Full_orig.csv'
json_path = r'c:\\CPU2BP\\CSR\\measurement_catalog.json'

# Load existing JSON
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find existing MMC5.1.0 entry and build a set of existing files per root
existing_entry = next((entry for entry in data if entry.get("name") == "MMC5.1.0"), None)
existing_files_by_root = defaultdict(set)
if existing_entry:
    for folder in existing_entry.get("folders", []):
        root = folder.get("root")
        for file in folder.get("files", []):
            existing_files_by_root[root].add(file)

def extract_name_from_line(line):
    match = re.search(r'5K45/([^/]+)/', line)
    if match:
        return match.group(1) + "___"
    return None

# Group new files by name and root
folders_by_name = {}

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for idx, row in enumerate(reader):
        # Find the file (endswith .MF4.xz)
        file_idx = next((i for i, p in enumerate(row) if p.lower().endswith('.mf4.xz')), None)
        if file_idx is None:
            print(f"No .MF4.xz file found in line {idx+1}: {row}")
            continue
        # Find the first non-empty part after the file as CPD_GT
        CPD_GT = None
        for j in range(file_idx + 1, len(row)):
            if row[j]:
                CPD_GT = row[j]
                break
        if CPD_GT is None:
            print(f"No CPD_GT after file in line {idx+1}: {row}")
            continue
        file_path = row[file_idx]
        name = extract_name_from_line(file_path)
        
        if not name:
            print(f"Could not extract name from line {idx+1}: {file_path}")
            continue
        root = file_path[:file_path.rfind('/')+1]
        file_name = file_path.split('/')[-1]
        # ...existing code for skipping existing files...
        if name not in folders_by_name:
            folders_by_name[name] = {}
        if root not in folders_by_name[name]:
            folders_by_name[name][root] = {
                "root": root,
                "files": [],
                "gt": {
                    "CPD_GT": CPD_GT,
                    "OC_Adult_GT": 0,
                    "OC_GT": 0,
                    "M_BLD_GT": 0,
                    "S_BLD_GT": 0,
                    "M_INTERFERENCE_GT": 0,
                    "S_INTERFERENCE_GT": 0
                }
            }
        folders_by_name[name][root]["files"].append(file_name)

# Remove any existing entries with those names, then add new ones
new_data = [entry for entry in data if entry.get("name") not in folders_by_name]
for name, folders_dict in folders_by_name.items():
    new_data.append({
        "name": name,
        "folders": list(folders_dict.values())
    })

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=4, ensure_ascii=False)

print(f"Added {sum(len(f['files']) for folders_dict in folders_by_name.values() for f in folders_dict.values())} files ")