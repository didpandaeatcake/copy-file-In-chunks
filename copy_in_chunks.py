import os
import argparse

def copy_large_file_resumable(source_path, destination_path, chunk_size=50):
    try:
        
        print(f"Source path: {source_path}")
        print(f"Destination path: {destination_path}")

        # file already exists
        if os.path.exists(destination_path):
            copied_bytes = os.path.getsize(destination_path)
            print(f"Resuming copy from {copied_bytes} bytes...")
        else:
            copied_bytes = 0

        # destination directory exists
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        # check write permissions
        if not os.access(os.path.dirname(destination_path), os.W_OK):
            print(f"Error: No write permissions for {os.path.dirname(destination_path)}")
            return

        # cp file in chunks
        with open(source_path, "rb") as source_file:
            with open(destination_path, "ab" if copied_bytes else "wb") as destination_file:
                source_file.seek(copied_bytes)  # move to the last copied byte
                while True:
                    chunk = source_file.read(1024 * 1024 * chunk_size)
                    if not chunk:
                        break
                    destination_file.write(chunk)
                    copied_bytes += len(chunk)
                    print(f"Copied {copied_bytes} bytes...")

        
        if os.path.exists(destination_path):
            print(f"File successfully copied to {destination_path}")
        else:
            print(f"Error: File was not created at {destination_path}")

    except PermissionError as e:
        print(f"Permission denied: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    
    parser = argparse.ArgumentParser(description="Copy large files in chunks with resumable support.")
    parser.add_argument("source", help="Path to the source file.")
    parser.add_argument("destination", help="Path to the destination file.")
    parser.add_argument("--chunk_size", type=int, default=50,
                        help="Chunk size in bytes (default: 50MB).")

    args = parser.parse_args()
    copy_large_file_resumable(args.source, args.destination, args.chunk_size)

if __name__ == "__main__":
    main()