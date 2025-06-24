import sys
import bitIO
import Encode

def decode_file(input_filename, output_filename):
    """
    Decodes a Huffman-encoded file and recreates the original file.
    """
    try:
        with open(input_filename, 'rb') as infile, open(output_filename, 'wb') as outfile:
            bitstreamin = bitIO.BitReader(infile)

            # Reads the frequency table
            frequency_table = [bitstreamin.readint32bits() for _ in range(256)]

            # Calculates the total number of bytes in the frequency table. If empty, return
            total_bytes = sum(frequency_table)
            if total_bytes == 0:
                return

            # Builds the Huffman tree based on the frequency table
            huffman_tree_root = Encode.build_huffman_tree(frequency_table)

            # Initializes variables for decoding
            total_bytes = sum(frequency_table)
            bytes_written = 0
            current_node = huffman_tree_root

            # Processes the encoded bitstream and decodes it back to the original bytes
            while bytes_written < total_bytes:

                # If the tree has only one node, it writes all bytes directly
                if huffman_tree_root.left is None and huffman_tree_root.right is None:
                    outfile.write(bytes([huffman_tree_root.byte] * total_bytes))
                    break
                else: 
                    # Reads the next bit and checks if it was read successfully
                    bit = bitstreamin.readbit()
                    if not bitstreamin.readsucces():
                        break

                    # Traverses the Huffman tree based on the bit read
                    if bit == 0:
                        current_node = current_node.left
                    else:
                        current_node = current_node.right
                    
                    # If a leaf node is reached, it writes the corresponding byte to the output file
                    if current_node.left is None and current_node.right is None:
                        outfile.write(bytes([current_node.byte]))
                        bytes_written += 1
                        current_node = huffman_tree_root

    except FileNotFoundError:
        # Handles when the input file is not found
        print(f"File '{input_filename}' not found.")
        sys.exit(1)


if __name__ == "__main__": 
    # Ensures the script is called with exactly two arguments (input and output filenames)
    if len(sys.argv) != 3:
        print("Usage: python decode.py <inputfile> <outputfile>")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    # Call the decode function with the provided filenames
    decode_file(input_filename, output_filename)
    print(f"Decoded {input_filename} to {output_filename}")
