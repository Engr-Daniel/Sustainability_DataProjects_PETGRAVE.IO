import os
import json

# Path to the "savedjson" folder
base_folder = "savedjson"

# Initialize a list to store data from all state files
nigeria_data = []

# Loop through all files in the "savedjson" folder
for file_name in os.listdir(base_folder):
    # Check if the file is a JSON file and not a folder
    if file_name.endswith(".json") and os.path.isfile(os.path.join(base_folder, file_name)):
        file_path = os.path.join(base_folder, file_name)
        
        # Skip the nigeria.json file if it already exists
        if file_name == "nigeria.json":
            continue
        
        # Read and load the JSON file
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                nigeria_data.extend(data)  # Add data to the combined list
            except json.JSONDecodeError as e:
                print(f"Error reading {file_path}: {e}")

# Write the combined data to a new JSON file named "nigeria.json"
output_file = os.path.join(base_folder, "nigeria.json")
with open(output_file, "w", encoding="utf-8") as output:
    json.dump(nigeria_data, output, ensure_ascii=False, indent=4)

print("Merged data saved to nigeria.json!")
