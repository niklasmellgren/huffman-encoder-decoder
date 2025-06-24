''' 
Group: Niklas Mellgren
SDU-login: nimel11
'''


import sys


def parent(i):
    """Calculates the parent index of a given index in a heap."""
    return (i - 1) // 2


def left(i):
    """Calculates the left child index of a given index in a heap."""
    return 2 * i + 1


def right(i):
    """Calculates the right child index of a given index in a heap."""
    return 2 * i + 2


def min_heapify(A, i):
    """
    Iteratively maintains the min-heap property for a heap at a given node index.
    """
    size = len(A)
    while True:
        l = left(i)
        r = right(i)
        smallest = i

        if l < size and A[l] < A[i]:
            smallest = l
        if r < size and A[r] < A[smallest]:
            smallest = r
        if smallest != i:
            A[i], A[smallest] = A[smallest], A[i]
            i = smallest
        else:
            break


def extractMin(A):
    """
    Removes and returns the minimum element from the heap.
    Raises an exception if the heap is empty.

    PS.
    I know that the 'if' statement from the pseudo code could be left out,
    but to prevent potential runtime errors in the future,
    I have included a raise Exception implementation.
    """
    if not A:
        raise Exception("Cannot extract from an empty heap.")
    min_element = A[0]
    last_element = A.pop()
    if A:
        A[0] = last_element
        min_heapify(A, 0)
    return min_element


def insert(A, key):
    """Inserts a new element into the heap."""
    A.append(key)
    i = len(A) - 1
    while i > 0 and A[parent(i)] > A[i]:
        A[i], A[parent(i)] = A[parent(i)], A[i]
        i = parent(i)


def createEmptyPQ():
    """Returns a new, empty priority queue."""
    return []


def main():
    """
    Reads numbers from a specified file, inserts them into a min-heap,
    and then attempts to extract them in ascending order.

    Usage (type in command line):
    python scriptname.py filename.txt

    Example:
    python pqheap.py mixed.txt
    """
    if len(sys.argv) < 2:
        print("Usage: python scriptname.py filename.txt (type in command line)")
        print("Example: python pqheap.py mixed.txt")
        sys.exit(1)

    filename = sys.argv[1]

    A = createEmptyPQ()
    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.strip():
                    insert(A, int(line.strip()))
    except FileNotFoundError:
        print(f"File {filename} not found.")
        sys.exit(1)

    if not A:
        print("Cannot extract from an empty heap.")
    else:
        print("Extracted in order:")
        while A:
            print(extractMin(A))


if __name__ == "__main__":
    main()
