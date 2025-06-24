'''
Group: Niklas Mellgren
SDU-login: nimel11
'''


import sys
import bitIO
from Element import Element
import PQHeap

class Node:
    """
    A node in the Huffman tree containing left and right child,
    byte value, and frequency.
    """
    
    def __init__(self, left=None, right=None, byte=None, freq=0):
        self.left = left # Left child node
        self.right = right # Right child node
        self.byte = byte # For leaf nodes. This stores the byte value
        self.freq = freq # For internal nodes. This stores the frequency

def build_frequency_table(filename):
    """
    Builds a frequency table from the bytes read from a file.
    Each index corresponds to a byte value (0-255),
    and the value at each index represents the frequency
    of that byte in the file.
    """
    frequency = [0] * 256 # Initializes frequency table with zeros
    
    try:
        with open(filename, 'rb') as file:
            byte = file.read(1)
            while byte:
                frequency[byte[0]] += 1 # byte[0] is treated as an integer representing the byte
                byte = file.read(1)
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)
    return frequency

def build_huffman_tree(frequency_table):
    """
    Constructs a Huffman tree based on the frequency table. 
    Uses a priority queue to combine nodes with the lowest 
    frequencies until a single tree is formed. 
    Handles edge cases for empty files or files with a single unique byte.
    """
    pq = PQHeap.createEmptyPQ()

    # Creates leaf nodes for each byte with non-zero frequency 
    # and inserts them into the priority queue
    for byte, freq in enumerate(frequency_table):
        if freq > 0:
            node = Node(byte=byte, freq=freq)
            PQHeap.insert(pq, Element(freq, node)) # Inserts Element objects with frequency as key

    n = len(pq)

    # Handles an empty file or a file with only one unique byte
    if n == 0:
        return None  
    elif n == 1:
        single_node = PQHeap.extractMin(pq).data
        return Node(left=single_node, right=None, byte=single_node.byte, freq=single_node.freq)

    # Combines nodes with the lowest frequencies until a single tree is formed
    for _ in range(n - 1):
        x = PQHeap.extractMin(pq).data
        y = PQHeap.extractMin(pq).data
        z = Node(left=x, right=y, freq=x.freq + y.freq)
        PQHeap.insert(pq, Element(z.freq, z))

    return PQHeap.extractMin(pq).data # The root of the Huffman tree

def generate_huffman_codes(node, code="", code_table=None):
    """
    Generates the Huffman codes for each byte using an in-order traversal of the Huffman tree.
    The codes are determined by the path taken to reach each leaf node,
    using '0' for left and '1' for right traversals.
    """
    if code_table is None:
        code_table = [""] * 256  # Initializes code table with empty strings

    if node is None:
        return code_table

    # Traverses the left subtree
    if node.left:
        generate_huffman_codes(node.left, code + "0", code_table)

    # Processes the current node if it's a leaf
    if node.left is None and node.right is None:
        code_table[node.byte] = code  # Assigns code to the leaf node

    # Traverses the right subtree
    if node.right:
        generate_huffman_codes(node.right, code + "1", code_table)

    return code_table

def write_encoded_file(input_filename, output_filename, frequency_table, huffman_codes):
    """
    Writes an encoded file using Huffman codes. 
    The file begins with a frequency table,
    followed by the encoded data.
    """
    with open(input_filename, 'rb') as input_file, open(output_filename, 'wb') as output_file:
        bit_writer = bitIO.BitWriter(output_file)
        
        # Writes the frequency table to the output file
        for freq in frequency_table:
            bit_writer.writeint32bits(freq)
        
        # Reads the input file and writes the encoded data
        byte = input_file.read(1)
        while byte:
            byte_value = byte[0]
            code = huffman_codes[byte_value]  # List indexing to access the Huffman code
            for bit in code:
                bit_writer.writebit(int(bit))
            byte = input_file.read(1)
        bit_writer.close()


if __name__ == "__main__":
    # Ensures the script is called with exactly two arguments (input and output filenames)
    if len(sys.argv) != 3:
        print("Usage: python encode.py <inputfile> <outputfile>")
        sys.exit(1)
    
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    
    # Builds the frequency table from the input file
    frequency_table = build_frequency_table(input_filename)

    # Builds the Huffman tree from the frequency table
    huffman_tree_root = build_huffman_tree(frequency_table)

    # Handles edge cases for empty or single-byte files
    if huffman_tree_root is None:
        with open(output_filename, 'wb') as output_file:
            bit_writer = bitIO.BitWriter(output_file)
            for freq in frequency_table:
                bit_writer.writeint32bits(freq)
            bit_writer.close()
    else:
        # Generates Huffman codes from the Huffman tree
        huffman_codes = generate_huffman_codes(huffman_tree_root)

        # Writes the encoded file
        write_encoded_file(input_filename, output_filename, frequency_table, huffman_codes)
        print(f"Encoded {input_filename} to {output_filename}")
