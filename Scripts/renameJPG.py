import os
import re

def rename_jpg_files(directory, nameToChange):
    # Get a list of all .jpg files in the directory
    match = re.match(r"(.*?)(\d+)$", nameToChange)
    if not match:
        print("Invalid base name format. It should end with a number.")
        return
    
    base_name, start_number = match.groups()
    start_number = int(start_number)
    
    # Trier les fichiers
    jpg_files = sorted([f for f in os.listdir(directory) if f.lower().endswith('.jpg')])
    
    for index, filename in enumerate(jpg_files, start=start_number):
        new_name = f"{base_name}{index}.jpg"
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)
        
        try:
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_name}")
        except Exception as e:
            print(f"Error renaming {filename}: {e}")

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ").strip()
    name_to_change = input("Enter the new base name for files: ").strip()
    
    if os.path.exists(folder_path):
        rename_jpg_files(folder_path, name_to_change)
    else:
        print("Invalid folder path.")
