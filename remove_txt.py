import os

# Set the directory path
dir_path = "./txt_files"

# Loop through all files in the directory
for file_name in os.listdir(dir_path):
    # Check if the file is a .txt file
    if file_name.endswith(".txt"):
        # Remove the file
        os.remove(os.path.join(dir_path, file_name))