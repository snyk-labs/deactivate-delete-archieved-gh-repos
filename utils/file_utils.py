import json

def write_json_to_file(data, file_path):
    """Write JSON data to a file."""
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully written to {file_path}")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}") 