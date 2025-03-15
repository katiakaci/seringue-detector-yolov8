import os

def rename_jpg_files(directory, nameToChange):
    # Get a list of all .jpg files in the directory
    jpg_files = sorted([f for f in os.listdir(directory) if f.lower().endswith('.jpg')])
    
    for index, filename in enumerate(jpg_files, start=1):
        new_name = f"{nameToChange}{index}.jpg"
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
