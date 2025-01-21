def lz77_compress(text, window_size, max_match_length):

    i=0
    text_length=len(text)
    token=[0, 0, text[0]]
    token_seq=[]
    token_seq.append(token)
    search_buffer=text[0]
    i+=1

    while i < text_length-1:
        if text[i] in search_buffer:
            current_buffer=text[i]
            matched_buffer=''

            while current_buffer in search_buffer and len(current_buffer) < max_match_length+1:
                matched_buffer=current_buffer
                if i==text_length-1: #current_buffer reached the end + still matches
                    break
                current_buffer=current_buffer+text[i+1]
                i+=1
            matched_length=len(matched_buffer)
            matched_offset=i-matched_length-search_buffer.rfind(matched_buffer)
            literal=current_buffer[len(current_buffer)-1]

            if i == text_length-1:
                if current_buffer == matched_buffer:
                    matched_offset+=1
                    literal='None'
                    print(matched_buffer)

            token=[matched_offset, matched_length, literal]
            token_seq.append(token)
            search_buffer=search_buffer+matched_buffer
            if len(search_buffer)>window_size:
                search_buffer = search_buffer[-window_size:]

            i+=1 #skip literal

        else:
            token=[0, 0, text[i]]
            token_seq.append(token)
            search_buffer = search_buffer+text[i]
            if len(search_buffer)>window_size:
                search_buffer = search_buffer[-window_size:]
            i+=1
    print(token_seq)

text='ABCDEABCDEFGABCDEABCDD'
print(text)
lz77_compress(text, 100, 10)
print("\n\n")
