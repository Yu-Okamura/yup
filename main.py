import heapq


print('Program started.')

def convert_to_binary():
    with open('content.txt', 'r', encoding='utf-8') as f:
        f_origin=f.read()
        print('original: '+f_origin)
    f_utf8=f_origin.encode('utf-8')
    print('utf-8: '+str(f_utf8))
    f_binary=''.join(format(byte, '08b') for byte in f_utf8)
    print('binary: '+str(f_binary))
    return f_binary

def split_bit4(binary_seq):
    binary_bit4=[binary_seq[i:i+4] for i in range(0, len(binary_seq), 4)]
    print(binary_bit4)
    return binary_bit4

split_bit4(convert_to_binary())
