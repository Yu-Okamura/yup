import zipfile
from transformers import AutoTokenizer
import zlib
import numpy as np
import os

def compare_with_zip(filename, filepath_zip):
    with zipfile.ZipFile(filepath_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(filename, arcname=filename.split("/")[-1])
    file_size_original=os.path.getsize(filename)
    file_size_zip=os.path.getsize(filepath_zip)
    compression_ratio_zip = (file_size_zip/file_size_original)*100
    print('Original file size: '+str(file_size_original)+' bytes')
    print('Zip file size: '+str(file_size_zip)+' bytes')
    print('Zip compression ratio: '+str(round(compression_ratio_zip, 0))+'%')
    return 0

def decimal_to_base(numbers, base):
    return [np.base_repr(number, base=base) for number in numbers]


def tokenize(text):

    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    tokenized_text_list = tokenizer.encode(text, add_special_tokens=True)

    tokens_to_string = tokenizer.convert_ids_to_tokens(tokenized_text_list)

    tokenized_text_list_base7 = decimal_to_base(tokenized_text_list, 7)
    tokenized_text = ",".join(map(str, tokenized_text_list_base7))

    return tokenized_text

def deflate(binary_seq):
    deflate_output = zlib.compress(binary_seq, 9)
    deflate_output = ''.join(format(byte, '08b') for byte in deflate_output)
    return deflate_output

"""
def inflate(deflate_output):


    return inflate_output
"""

def main():

    filename='content.txt'
    with open(filename, 'r', encoding='utf-8') as f:
        text=f.read()

    text = text.replace('. ', ' ')
    text = text.replace(', ', ' ')

    tokenized_text=tokenize(text)
    token_binary=tokenized_text.encode('utf-8')
    deflate_tokene=deflate(token_binary)
    print('The size after tokenized+zlib: '+ str(len(deflate_tokene)/8)+' bytes')

    filepath_zip='content.zip'
    compare_with_zip(filename, filepath_zip)



if __name__ == '__main__':
    main()
