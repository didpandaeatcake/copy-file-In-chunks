import os
import argparse
import shutil  # For cross-platform disk space check
from tqdm import tqdm  # For the progress bar

def copy_large_file_resumable(source_path, destination_path, chunk_size=50):
    try:
        print(f"Source path: {source_path}")
        print(f"Destination path: {destination_path}")

        # Validate source path
        if not os.path.isfile(source_path):
            print(f"Error: Source file '{source_path}' does not exist.")
            return

        # Validate destination path
        destination_dir = os.path.dirname(destination_path)
        if not os.path.isdir(destination_dir) and destination_dir:
            print(f"Error: Destination directory '{destination_dir}' does not exist.")
            return

        # Validate chunk size
        if chunk_size <= 0:
            print("Error: Chunk size must be greater than zero.")
            return

        # Check disk space using shutil.disk_usage (cross-platform)
        total, used, free = shutil.disk_usage(destination_dir or os.getcwd())
        source_size = os.path.getsize(source_path)
        if free < source_size:
            print("Error: Not enough space on the destination drive.")
            return

        # Check if destination file exists and its size
        copied_bytes = os.path.getsize(destination_path) if os.path.exists(destination_path) else 0
        if copied_bytes > 0:
            print(f"Resuming copy from {copied_bytes} bytes...")

        # Copy in chunks with a progress bar
        with open(source_path, "rb") as source_file, open(destination_path, "ab" if copied_bytes else "wb") as destination_file:
            source_file.seek(copied_bytes)

            with tqdm(total=source_size, initial=copied_bytes, unit='B', unit_scale=True, desc="Copying") as progress:
                while True:
                    chunk = source_file.read(1024 * 1024 * chunk_size)
                    if not chunk:
                        break
                    destination_file.write(chunk)
                    copied_bytes += len(chunk)
                    progress.update(len(chunk))  # Update progress bar

        print(f"\nFile successfully copied to {destination_path}")

    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except PermissionError as e:
        print(f"Permission denied: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Copy large files in chunks with resumable support.")
    parser.add_argument("source", help="Path to the source file.")
    parser.add_argument("destination", help="Path to the destination file.")
    parser.add_argument("--chunk_size", type=int, default=50,
                        help="Chunk size in MB (default: 50MB).")

    args = parser.parse_args()
    copy_large_file_resumable(args.source, args.destination, args.chunk_size)

if __name__ == "__main__":
    main()
