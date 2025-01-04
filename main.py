print('Program started.')

def convert_to_binary():
    with open('content.txt', 'r', encoding='utf-8') as f:
        f_origin=f.read()
        print('original: '+f_origin)
    f_utf8=f_origin.encode('utf-8')
    print('utf-8: '+str(f_utf8))
    f_binary=''.join(format(byte, '08b') for byte in f_utf8)
    print('binary: '+str(f_binary))
    return(f_binary)

convert_to_binary()
