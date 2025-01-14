import os
import json

# Path to the "savedjson" folder
base_folder = "savedjson"

# Loop through each state folder
for state in os.listdir(base_folder):
    state_folder = os.path.join(base_folder, state)
    
    # Check if it's a folder
    if os.path.isdir(state_folder):
        combined_data = []  # List to store all recycling company details for the state

        # Loop through each JSON file in the state folder
        for json_file in os.listdir(state_folder):
            if json_file.endswith(".json"):  # Ensure it's a JSON file
                file_path = os.path.join(state_folder, json_file)
                
                # Read and load the JSON file
                with open(file_path, "r", encoding="utf-8") as file:
                    try:
                        data = json.load(file)
                        combined_data.extend(data)  # Append the data to the combined list
                    except json.JSONDecodeError as e:
                        print(f"Error reading {file_path}: {e}")

        # Write the combined data to a new JSON file named after the state
        output_file = os.path.join(base_folder, f"{state}.json")
        with open(output_file, "w", encoding="utf-8") as output:
            json.dump(combined_data, output, ensure_ascii=False, indent=4)

print("Merging complete!")
