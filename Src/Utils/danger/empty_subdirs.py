import os
import shutil

# Define the base directory
base_dir = "Data/Tickers"

# Iterate over all subdirectories in the base directory
for subdir, dirs, files in os.walk(base_dir):
    # Iterate over all files in the current subdirectory
    for file in files:
        # Create the file path by joining the subdirectory and file name
        file_path = os.path.join(subdir, file)

        # Delete the file
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        except Exception as e:
            print(f"Error deleting file: {file_path}. Reason: {e}")

print("All files in subdirectories of 'Data/Tickers' have been deleted.")
