# copy-file-In-chunks
**Python script to copy large file in chunks**

Some older file systems or specific storage devices (e.g., FAT32) have a **maximum file size limit**, often around **4GB**. Additionally, some network drives or protocols may impose restrictions on the size of files that can be transferred in a single operation. By using a **chunked file copy method**, you can bypass these limitations by transferring the file in smaller, manageable pieces. This approach not only helps you work around size restrictions but also provides better control over the transfer process, such as resuming interrupted transfers or monitoring progress.


```
python copy_in_chunks.py source_file_location destination_location

python copy_in_chunks.py "C:\testfile.txt" "X:\testfile.txt"  --chunk_size [optional default 50MB]

```
if you want 50MB chunk size, it is set by default, in case 100MB then 

```

python copy_in_chunks.py "C:\testfile.txt" "X:\testfile.txt"  --chunk_size 100

```

## How Chunked Copying Works


1. The file is divided into smaller chunks (e.g., 50MB, 100MB).
2. Each chunk is transferred individually.
3. The chunks are reassembled at the destination to recreate the original file.

---


