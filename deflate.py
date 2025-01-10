import heapq
from collections import defaultdict

# LZ77 Compression
def lz77_compress(data, window_size=20):
    compressed = []
    i = 0
    while i < len(data):
        match_length = 0
        match_distance = 0

        # Search for matches in the sliding window
        for j in range(max(0, i - window_size), i):
            length = 0
            while length < len(data) - i and data[j + length] == data[i + length]:
                length += 1

            if length > match_length:
                match_length = length
                match_distance = i - j

        if match_length > 0:
            compressed.append((match_distance, match_length, data[i + match_length] if i + match_length < len(data) else ""))
            i += match_length + 1
        else:
            compressed.append((0, 0, data[i]))
            i += 1

    return compressed

# Huffman Coding
class HuffmanNode:
    def __init__(self, symbol, freq):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequencies):
    heap = [HuffmanNode(symbol, freq) for symbol, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

def build_huffman_codes(node, prefix="", code_map={}):
    if node is not None:
        if node.symbol is not None:
            code_map[node.symbol] = prefix
        build_huffman_codes(node.left, prefix + "0", code_map)
        build_huffman_codes(node.right, prefix + "1", code_map)
    return code_map

def huffman_compress(data):
    # Calculate frequency of each 4-bit group
    frequencies = defaultdict(int)
    for symbol in data:
        frequencies[symbol] += 1

    # Build the Huffman Tree and generate codes
    root = build_huffman_tree(frequencies)
    huffman_codes = build_huffman_codes(root)

    # Encode the data
    encoded_data = "".join(huffman_codes[symbol] for symbol in data)
    print(len(str(encoded_data)))
    return encoded_data, huffman_codes

# Split binary input into groups of 4 bits
def split_into_4bit_groups(binary_data):
    return [binary_data[i:i+4] for i in range(0, len(binary_data), 4)]

def main():
    binary_input = "00010000000110110010000000100011101100100000000000111011000100000011011110110111000010011001101101100010010100011011000100000001001010110001000000100001000000011011001000000010001110110010000000000011101100010000001101111011011100001001100110110110001001010001101100010000000100101011000100000010000100000001101100100000001000111011001000000000001110110001000000110111101101110000100110011011011000100101000110110001000000010010101100010000001000010000000110110010000000100011101100100000000000111011000100000011011110110111000010011001101101100010010100011011000100000001001010110001000000100001000000011011001000000010001110110010000000000011101100010000001101111011011100001001100110110110001001010001101100010000000100101011000100000010000100000001101100100000001000111011001000000000001110110001000000110111101101110000100110011011011000100101000110110001000000010010101100010000001000010000000110110010000000100011101100100000000000111011000100000011011110110111000010011001101101100010010100011011000100000001001010110001000000100001000000011011001000000010001110110010000000000011101100010000001101111011011100001001100110110110001001010001101100010000000100101011000100000010000100000001101100100000001000111011001000000000001110110001000000110111101101110000100110011011011000100101000110110001000000010010101100010000001000010000000110110010000000100011101100100000000000111011000100000011011110110111000010011001101101100010010100011011000100000001001010110001000000100001000000011011001000000010001110110010000000000011101100010000001101111011011100001001100110110110001001010001101100010000000100101011000100000010"
    print(len(str(binary_input)))

    # Step 1: Split into groups of 4 bits
    groups = split_into_4bit_groups(binary_input)

    # Step 2: Apply LZ77 Compression
    lz77_output = lz77_compress(groups)

    # Flatten LZ77 output for Huffman coding
    flat_lz77 = []
    for distance, length, symbol in lz77_output:
        flat_lz77.append(f"({distance},{length})")
        if symbol:
            flat_lz77.append(symbol)

    # Step 3: Apply Huffman Coding
    huffman_encoded, huffman_codes = huffman_compress(flat_lz77)

    print("Original Binary Input:", binary_input)
    print("Groups of 4 bits:", groups)
    print("LZ77 Compressed Output:", lz77_output)
    print("Huffman Encoded Output:", huffman_encoded)
    print("Huffman Codes:", huffman_codes)

if __name__ == "__main__":
    main()
