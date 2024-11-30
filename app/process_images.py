import os
import shutil
from datetime import datetime
import exiftool

# File counters
copied_count = 0
skipped_count = 0

def create_dir_structure(base_path, year, month, day):
    """
        Creates the folder structure
    """
    year_path = os.path.join(base_path, year)
    month_path = os.path.join(year_path, month)
    day_path = os.path.join(month_path, day)

    os.makedirs(day_path, exist_ok=True)
    return day_path

def extract_date_with_exiftool(file_path):
    """
        Extracts creation date with ExifToolHelper
    """
    try:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata(file_path)  # Devuelve una lista
            if metadata_list and isinstance(metadata_list, list):
                metadata = metadata_list[0]  # Selecciona el primer elemento
                date_str = metadata.get('EXIF:DateTimeOriginal') or \
                    metadata.get('EXIF:CreateDate') or \
                    metadata.get('XMP:CreateDate') or \
                    metadata.get('DateTimeOriginal') or \
                    metadata.get('Create Date') or \
                    metadata.get('QuickTime:CreateDate')
                if date_str:
                    return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
    except Exception as e:
        print(f"ERROR: error extracting metadata with for {file_path}: {e}")
    return None

def copy_file_if_not_exists(src, dest):
    """
        Copies (using copy2) or moves (using move) the file if it isn't exist
        Changes the comments, depending on your preference for copying or moving
    """
    global copied_count, skipped_count
    if not os.path.exists(dest):
        # shutil.copy2(src, dest)
        shutil.move(src, dest)
        copied_count += 1
        # print(f"Copied: {src} -> {dest}")
        print(f"Moved: {src} -> {dest}")
    else:
        skipped_count += 1
        print(f"Skipped (existing files): {src}")

def process_file(file_path, dest_base):
    """
        Porcces the file using ExifTool
    """
    date = extract_date_with_exiftool(file_path)
    if not date:
        print(f"Not possible to extract the date for {file_path}.")
        return

    dest_path = create_dir_structure(dest_base, str(date.year), f"{date.month:02d}", f"{date.day:02d}")
    dest_file_path = os.path.join(dest_path, os.path.basename(file_path))
    copy_file_if_not_exists(file_path, dest_file_path)

def main():
    global copied_count, skipped_count
    source_dir = os.environ.get("SOURCE_DIR", "/data/PHOTOS_TEMP/")
    dest_dir = os.environ.get("DEST_DIR", "/data/PHOTOS/")

    source_dir = os.path.expanduser(source_dir)
    dest_dir = os.path.expanduser(dest_dir)

    for root, _, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            # Add more extensions if needed.
            if file.lower().endswith(('.jpg', '.jpeg', '.raw', '.dng', '.nef', '.crw', '.cr2', '.arw', '.mrw', '.heic', '.mp4')):
                process_file(file_path, dest_dir)

    # Final Summary
    print("\n=== Execution results ===")
    print(f"Files copied/moved: {copied_count}")
    print(f"Skipped files (existing files): {skipped_count}")

if __name__ == "__main__":
    main()