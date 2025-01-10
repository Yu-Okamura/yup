import zipfile
import os
import heapq
from collections import Counter
import pickle
import zlib
from transformers import AutoTokenizer
import numpy as np

def zipfy(filename, file_zip):
    with zipfile.ZipFile(file_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(filename, arcname=filename.split("/")[-1])
        print(f"{file_zip} created.")
    return 0

def convert_to_binary(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        f_origin=f.read()
        # print('original: '+f_origin)
    f_utf8=f_origin.encode('utf-8')
    # print('utf-8: '+str(f_utf8))
    f_binary=''.join(format(byte, '08b') for byte in f_utf8)
    # print('binary: '+str(f_binary))
    # print('length of original binary: '+str(len(f_binary)))
    return f_binary

def split_binary_seq_bit_blocks(binary_seq, block_size):
    binary_binary_seq_bit_blocks=[binary_seq[i:i+block_size] for i in range(0, len(binary_seq), block_size)]
    # print(binary_binary_seq_bit_blocks)
    return binary_binary_seq_bit_blocks

def count_frequencies(binary_seq_bit_blocks):
    bit_block_frequencies = Counter(binary_seq_bit_blocks)
    # print("Frequency of each bit block:", frequency)
    return bit_block_frequencies

class HuffmanNode:
    def __init__(self, block, freq):
        self.block = block
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(bit_block_frequencies):

    heap = [HuffmanNode(block, freq) for block, freq in bit_block_frequencies.items()]
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

def huffman_encode(binary_seq_bit_blocks, huffman_codes):
    encoded_binary=''.join(huffman_codes[block] for block in binary_seq_bit_blocks)
    # print('Encoded binary: '+encoded_binary)
    # print('length of encoded binary: '+str(len(encoded_binary)))
    return encoded_binary

def deflate(token_seq):
    flat_list = [item for sublist in token_seq for item in sublist]
    token_frequencies = count_frequencies(flat_list)
    huffman_tree_root = build_huffman_tree(token_frequencies)
    huffman_codes = generate_huffman_codes(huffman_tree_root)
    encoded_binary=huffman_encode(flat_list, huffman_codes)

    return encoded_binary

def decimal_to_base(numbers, base):
    return [np.base_repr(number, base=base) for number in numbers]

def tokenize(filename):
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    with open(filename, 'r', encoding='utf-8') as f:
        text=f.read()
    tokenized_text_list = tokenizer.encode(text, add_special_tokens=True)
    tokenized_text_list_base7 = decimal_to_base(tokenized_text_list, 7)
    tokenized_text = ",".join(map(str, tokenized_text_list_base7))

    return tokenized_text

def tokens_to_bytes(input_string):

    token_bits = (input_string
        .replace(',', '000')
        .replace('0', '001')
        .replace('1', '010')
        .replace('2', '011')
        .replace('3', '100')
        .replace('4', '101')
        .replace('5', '110')
        .replace('6', '111')
    )
    token_bytes = token_bits.encode('utf-8')

    return token_bytes

def truncate_words_in_string(input_string):
    words = input_string.split(" ")  # Split by spaces
    result = []

    for word in words:
        if len(word) > 5:  # Check if the word is longer than 5 characters
            result.append(word[:5])  # Truncate the word to 5 characters
        else:
            result.append(word)  # Keep the word as is

    return " ".join(result)  # Rejoin the words into a string

def main():

    filename='content.txt'
    binary_seq=convert_to_binary(filename)
    file_size_original=os.path.getsize(filename)
    #print(binary_seq)
    print('The size of the original data: ' + str(file_size_original) + ' bytes')

    """omitting"""
    with open(filename, 'r', encoding='utf-8') as f:
        text=f.read()
    text = text.replace(' a ', ' ')
    text = text.replace(' is ', ' ')
    text = text.replace(' are ', ' ')
    text = text.replace(' were ', ' ')
    text = text.replace(' was ', ' ')
    text = text.replace(' is ', ' ')
    text = text.replace('ing ', 'i')
    text = text.replace('ed ', 'd')
    text = text.replace('. ', ' ')
    text = text.replace(', ', ' ')
    text=truncate_words_in_string(text)
    text = text.replace(' ', '')
    """print(text)"""
    text_deflate_compressed = zlib.compress(text.encode('utf-8'), -1)
    text_deflate_compressed = ''.join(format(byte, '08b') for byte in text_deflate_compressed)
    #print(text_deflate_compressed)
    print('The size after Omit+DEFLATE (zlib): '+ str(len(text_deflate_compressed)/8)+' bytes')


    """Zip"""
    zipfy(filename, 'content.zip')

    file_size_zip=os.path.getsize('content.zip')
    compression_ratio_zip = (file_size_zip/file_size_original)*100

    print('The size of the zipped data: ' + str(file_size_zip)+ ' bytes')
    print('The compression ratio: ' + str(round(compression_ratio_zip, 0)) + ' %')

    '''
    """Huffman encoding with 8 bit blocks"""
    file_original_binary=convert_to_binary(filename)
    binary_seq_bit_blocks=split_binary_seq_bit_blocks(file_original_binary, 8)
    bit_block_frequencies=count_frequencies(binary_seq_bit_blocks)
    huffman_tree_root = build_huffman_tree(bit_block_frequencies)
    huffman_codes = generate_huffman_codes(huffman_tree_root)
    encoded_binary=huffman_encode(binary_seq_bit_blocks, huffman_codes)

    size_huffman_codes_bits=len(str(huffman_codes))-len(huffman_codes)*6-(len(huffman_codes)-1)*2-2
    size_encoded_binary_bits=len(encoded_binary)
    size_total_huffman_bytes=(size_huffman_codes_bits+size_encoded_binary_bits)/8
    compression_ratio_huffman= (size_total_huffman_bytes/file_size_original)*100

    print('The size of the data after Huffman encoding (8-bits): '+ str(size_total_huffman_bytes)+' bytes') # this is approximation
    print('The compression ratio: '+ str(round(compression_ratio_huffman, 0)) + ' %')
    '''

    """DEFLATE (zlib)"""
    with open(filename, 'r', encoding='utf-8') as f:
        text=f.read()
    text_deflate_compressed = zlib.compress(text.encode('utf-8'), -1)
    text_deflate_compressed = ''.join(format(byte, '08b') for byte in text_deflate_compressed)
    #print(text_deflate_compressed)
    print('The size of the data after DEFLATE (zlib): '+ str(len(text_deflate_compressed)/8)+' bytes')

    """Tokenize + zlib"""
    tokenized_text=tokenize(filename)
    token_bytes=tokens_to_bytes(tokenized_text)
    #print(token_bytes)
    print('The size of the data after Tokenize: '+ str(len(token_bytes)/8)+' bytes')
    deflate_token_bytes=zlib.compress(token_bytes, -1)
    deflate_token_bytes=''.join(format(byte, '08b') for byte in deflate_token_bytes)
    #print(deflate_token_bytes)
    print('The size of the data after Tokenize + zlib: '+ str(len(deflate_token_bytes)/8)+' bytes')

    """Tokenize + huffman"""


if __name__ == "__main__":
    main()
