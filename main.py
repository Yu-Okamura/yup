import heapq
from collections import Counter

def convert_to_binary():
    with open('content.txt', 'r', encoding='utf-8') as f:
        f_origin=f.read()
        # print('original: '+f_origin)
    f_utf8=f_origin.encode('utf-8')
    # print('utf-8: '+str(f_utf8))
    f_binary=''.join(format(byte, '08b') for byte in f_utf8)
    # print('binary: '+str(f_binary))
    print('length of original binary: '+str(len(f_binary)))
    return f_binary

def split_bit_blocks(binary_seq, block_size):
    binary_bit_blocks=[binary_seq[i:i+block_size] for i in range(0, len(binary_seq), block_size)]
    # print(binary_bit_blocks)
    return binary_bit_blocks

def count_frequency(bit_blocks):
    frequency = Counter(bit_blocks)
    # print("Frequency of each bit block:", frequency)
    return frequency

class HuffmanNode:
    def __init__(self, block, freq):
        self.block = block
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequencies):

    heap = [HuffmanNode(block, freq) for block, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap) # extract the smallest + fixup
        right = heapq.heappop(heap) # extract the second smallest + fixup
        merged = HuffmanNode(None, left.freq + right.freq) # Establish new node w "None" block and combined freq
        merged.left = left # smallest -> left child
        merged.right = right # 2nd smallest -> right child
        heapq.heappush(heap, merged) #insert
    return heap[0]

def generate_huffman_codes(node, current_code="", codes=None):

    if codes is None:
        codes = {}

    """reached leaf node -> end"""
    if node.block is not None:
        codes[node.block] = current_code
        return codes

    if node.left is not None:
        generate_huffman_codes(node.left, current_code + "0", codes)
    if node.right is not None:
        generate_huffman_codes(node.right, current_code + "1", codes)

    return codes

def huffman_encode(binary_bit_blocks, huffman_codes):
    encoded_binary=''.join(huffman_codes[block] for block in binary_bit_blocks)
    # print('Encoded binary: '+encoded_binary)
    print('length of encoded binary: '+str(len(encoded_binary)))
    return encoded_binary


f_binary=convert_to_binary()

"""4bit blocks"""
print('\n4 bit block encoding:')
binary_bit_blocks=split_bit_blocks(f_binary, 4)
frequency=count_frequency(binary_bit_blocks)
huffman_tree_root = build_huffman_tree(frequency)
huffman_codes = generate_huffman_codes(huffman_tree_root)
# print('Huffman codes: '+ str(huffman_codes))
huffman_encode(binary_bit_blocks, huffman_codes)

"""8bit blocks"""
print('\n8 bit block encoding:')
binary_bit_blocks=split_bit_blocks(f_binary, 8)
frequency=count_frequency(binary_bit_blocks)
huffman_tree_root = build_huffman_tree(frequency)
huffman_codes = generate_huffman_codes(huffman_tree_root)
# print('Huffman codes: '+ str(huffman_codes))
huffman_encode(binary_bit_blocks, huffman_codes)

"""16bit blocks"""
print('\n16 bit block encoding:')
binary_bit_blocks=split_bit_blocks(f_binary, 16)
frequency=count_frequency(binary_bit_blocks)
huffman_tree_root = build_huffman_tree(frequency)
huffman_codes = generate_huffman_codes(huffman_tree_root)
# print('Huffman codes: '+ str(huffman_codes))
huffman_encode(binary_bit_blocks, huffman_codes)

print('\n\n\n')
