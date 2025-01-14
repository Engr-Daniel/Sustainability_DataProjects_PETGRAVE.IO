import os
import json

# Path to the "savedjson" folder
base_folder = "savedjson"

# Function to filter companies that have materials
def has_materials(company):
    return bool(company.get("materials", []))  # True if the materials list is not empty

# Process each JSON file in the folder
for file_name in os.listdir(base_folder):
    if file_name.endswith(".json"):  # Ensure it's a JSON file
        file_path = os.path.join(base_folder, file_name)

        # Read and filter the JSON file
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                # Filter companies with non-empty materials
                valid_companies = [company for company in data if has_materials(company)]
            except json.JSONDecodeError as e:
                print(f"Error reading {file_path}: {e}")
                continue

        # Create the new file name
        state_name = file_name.replace(".json", "")
        new_file_name = f"{state_name}_recycling_businesses.json"
        new_file_path = os.path.join(base_folder, new_file_name)

        # Write the filtered data to the new JSON file
        with open(new_file_path, "w", encoding="utf-8") as output:
            json.dump(valid_companies, output, ensure_ascii=False, indent=4)

print("Filtering complete! New files created with '_recycling_businesses' suffix.")
