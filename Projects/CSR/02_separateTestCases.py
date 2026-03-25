import json
import re
from collections import defaultdict

target_names = [
    "MMC_CPD_NCAP12_AWAKE_TP",
    "MMC_CPD_NCAP12_SLEEPING_TP",
    "MMC_CPD_NCAP12_ActivityAmbiguous_TP",
    "MMC_CPD_NCAP3_TP",
    "MMC_CPD_FP_ncap3",
    "MMC_CPD_FP_Adult",
    "MMC_CPD_FP_Adult_w_child",
    "MMC_CPD_FP_MovingToy",
    "MMC_CPD_FP_StaticToy",
    "MMC_CPD_FP_Bag",
    "MMC_CPD_FP_Liquid",
    "MMC_CPD_FP_Phone",
    "MMC_CPD_FP_Outside",
    "MMC_CPD_FP_Empty",
    "XC90_CPD_NCAP12_RainChamber",
    "XC90_CPD_FP_Adult_RainChamber",
    "XC90_CPD_FP_Adult_w_child_RainChamber",
    "XC90_CPD_FP_Empty_RainChamber",
    "MMC_CPD_FP_Empty_TEST"
]
file_path = r"c:\CPU2BP\CSR\MMC\newjson_02.json"

# Split each folder into multiple folders per TC, even if root is the same
def split_folders_by_tc(folders):
    tc_pattern = re.compile(r'([Tt][Cc]_?\d+)')
    new_folders = []
    for folder in folders:
        original_files = folder.get('files', {})
        if not isinstance(original_files, dict):
            # If files is not a dictionary, skip or handle as an error
            # For now, we'll just add the folder as is.
            new_folders.append(folder)
            continue

        tc_to_files = defaultdict(dict)
        no_tc_files = {}

        for filename, comment in original_files.items():
            match = tc_pattern.search(filename)
            if match:
                tc = match.group(1).upper() # Normalize TC name
                tc_to_files[tc][filename] = comment
            else:
                no_tc_files[filename] = comment

        # Add folders for each TC
        for tc, files_dict in tc_to_files.items():
            new_folders.append({
                "root": folder["root"],
                "files": files_dict,
                "gt": folder["gt"]
            })
        
        # Add a folder for files without TC, if any
        if no_tc_files:
            new_folders.append({
                "root": folder["root"],
                "files": no_tc_files,
                "gt": folder["gt"]
            })
            
    return new_folders

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find the target entries and process them
entries_found = 0
for entry in data:
    name = entry.get("name", "")
    if name in target_names and "folders" in entry:
        entries_found += 1
        folders = entry.get("folders", [])
        
        if isinstance(folders, list) and len(folders) > 0:
            # Check if the format seems to be the one we expect (dict of files)
            if all(isinstance(f.get('files'), dict) for f in folders if f):
                print(f"[INFO] Processing '{name}'...")
                entry["folders"] = split_folders_by_tc(folders)
            else:
                print(f"[WARNING] Skipping '{name}': 'files' is not a dictionary as expected or folder structure is mixed.")
        else:
            print(f"[INFO] Skipping '{name}': 'folders' is empty or not a list.")

if entries_found == 0:
    print(f"[ERROR] No target entries found in the JSON file.")
elif entries_found < len(target_names):
    print(f"[WARNING] Found and processed {entries_found} out of {len(target_names)} target entries.")

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print("Processing complete.")