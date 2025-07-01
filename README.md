# Huffman File Compressor

This project is a Python implementation of **Huffman coding**, a classic algorithm for compressing data without losing any information (lossless compression). It can compress and decompress any files — text, images, even DNA files.

The project showcases:
- How to read and write individual **bits** (not just bytes)
- How to use a **priority queue** (min-heap) to build a Huffman tree
- How to implement your own file compression tool from scratch

---

## How It Works
Huffman coding assigns shorter binary codes to frequent bytes and longer ones to rare bytes, reducing the overall file size.

### Encoding (Compressing a File)
1. Count how many times each byte appears in the file.
2. Build a Huffman tree using a priority queue.
3. Assign a binary code to each byte based on the tree.
4. Replace all the bytes in the file with their binary codes.
5. Write everything into a `.huf` file:
   - Frequency table (for decoding)
   - Encoded bits

### Decoding (Decompressing a File)
1. Read the frequency table from the `.huf` file.
2. Rebuild the same Huffman tree.
3. Read the bitstream and decode it back to the original bytes.

---

## File Overview

| File           | Purpose |
|----------------|---------|
| `Encode.py`    | Main encoder. Compresses any file using Huffman coding. |
| `Decode.py`    | Main decoder. Restores the original file from a `.huf` file. |
| `bitIO.py`     | Reads/writes individual bits and 32-bit integers. |
| `Element.py`   | Helper class for managing nodes in the priority queue. |
| `PQHeap.py`    | Custom priority queue (min-heap) used to build the Huffman tree. |

This project was created as part of the *DM507/DS814 Algorithms and Data Structures* course at the University of Southern Denmark.

- `bitIO.py` and `Element.py` were provided by Professor Rolf Fagerberg and are used without modifications.
- All other files and the overall implementation is done by me (Niklas Mellgren).
---

## How the Priority Queue (Min-Heap) Works

To build the Huffman tree, we need to repeatedly fetch the two least frequent symbols. A **min-heap** is ideal for this task because it efficiently keeps track of the smallest elements.

A **min-heap** is a binary tree where the **smallest item is always at the root**.  
In this project, the min-heap is implemented as a list, where index math is used to simulate parent-child relationships:

- **Left child** of index `i` → `2 * i + 1`  
- **Right child** of index `i` → `2 * i + 2`  
- **Parent** of index `i` → `(i - 1) // 2`

It supports:
- **Insertions** in `O(log n)`
- **Extracting the minimum** in `O(log n)`

The heap automatically reorders itself so that the smallest item “bubbles up” to the top after each operation.

---

## How to Use It

### Compress a file
```bash
python Encode.py inputfile.txt outputfile.huf
```

### Decompress the file
```bash
python Decode.py outputfile.huf decodedfile.txt
```

---

## Example

Try it with a test file in the `testfiles/` folder:

```bash
# Compress an image
python Encode.py testfiles/DolphinSunset.jpg testfiles/DolphinSunset.huf

# Decompress the result
python Decode.py testfiles/DolphinSunset.huf testfiles/DolphinSunset_decoded.jpg
```

After decompression, `DolphinSunset_decoded.jpg` will be identical to the original file.

---

## Notes

- Supports all file types: `.txt`, `.jpg`, `.pdf`, `.dna`, etc.
- Handles edge cases like:
  - Empty files
  - Files with only one unique byte

---
