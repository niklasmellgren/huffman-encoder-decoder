# Huffman File Compressor in Python

This repository contains a custom implementation of **Huffman coding** to compress and decompress binary files. The project demonstrates bit-level I/O handling, priority queues, and tree-based encoding for efficient lossless data compression.

## Overview

Two programs are included:
- `Encode.py` – Compresses a file using Huffman coding.
- `Decode.py` – Decompresses a previously compressed file.

Compression is performed by:
1. Scanning the input file to build a frequency table of bytes.
2. Constructing a Huffman tree from the table.
3. Generating Huffman codes via a recursive traversal.
4. Writing the frequency table and the encoded bitstream to the output.

Decompression reconstructs the original file by:
1. Reading the stored frequency table.
2. Rebuilding the same Huffman tree.
3. Reading bits from the file and traversing the tree to decode bytes.

## File Descriptions

| File           | Description |
|----------------|-------------|
| `Encode.py`    | Main encoder that builds a frequency table and compresses files using Huffman coding. |
| `Decode.py`    | Main decoder that reconstructs original data from a Huffman-compressed file. |
| `bitIO.py`     | Custom bit-level I/O utilities for reading/writing individual bits and 32-bit integers. |
| `Element.py`   | A small wrapper class with total ordering, used in the priority queue. |
| `PQHeap.py`    | A min-heap priority queue implementation used to construct the Huffman tree. |

## Usage

### Encode
```bash
python Encode.py inputfile.txt outputfile.huf
```

### Decode
```bash
python Decode.py outputfile.huf decodedfile.txt
```

### Example

You can try the tool using the included sample file `testfiles/dolphinsunset.jpg`:

```bash
# Compress the file
python Encode.py testfiles/dolphinsunset.jpg testfiles/dolphinsunset.huf
```

```bash
# Decompress it
python Decode.py testfiles/dolphinsunset.huf testfiles/dolphinsunset_decoded.jpg
```

All files must be opened in **binary mode**, and the encoded file will contain:
1. 256 integers (32-bit each) representing byte frequencies.
2. The bit-encoded body of the original file.

## Notes

- Works on all file types: `.txt`, `.jpg`, `.pdf`, etc.
- Optimized for clarity, modularity, and correct handling of corner cases (e.g., empty files or single-byte files).

## Acknowledgments
This project was built as part of the *DM507/DS814 Algorithms and Data Structures* course at the University of Southern Denmark.
- `bitIO.py` and `Element.py` were provided by Professor Rolf Fagerberg and are included without modifications.
- The remaining files and implementation were written by me (Niklas Mellgren) as part of the final project.
