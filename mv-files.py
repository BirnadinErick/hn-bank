import sys
import os
import shutil

# Create the "files" directory if it doesn't exist
os.makedirs("files", exist_ok=True)

# Get the filenames to be moved
MANIFEST = sys.argv[1]
with open(MANIFEST, "r") as m:
    d_files = [f for f in m.read().split(",")]

# Get a list of all files in the current working directory
files_to_move = [filename for filename in d_files if os.path.isfile(filename)]

# Move each file to the "files" directory
for filename in files_to_move:
    try:
        shutil.move(filename, os.path.join("files", filename))
        print(f"Moved {filename} to files/")
    except Exception as e:
        print(f"Error moving {filename}: {str(e)}")
