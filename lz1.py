def lz77_compress(text, window_size, max_match_length):

    i=0
    text_length=len(text)
    token=[0, 0, text[0]]
    token_seq=[]
    token_seq.append(token)
    search_buffer=text[0]
    i+=1

    while i<text_length-1:
        if text[i] in search_buffer:
            current_index=i
            current_buffer=text[current_index]
            matched_buffer=''

            while current_buffer in search_buffer and current_index<text_length-1:
                current_index+=1
                matched_buffer=current_buffer
                current_buffer=current_buffer+text[current_index]

            match_index_start_distance=i-search_buffer.rfind(matched_buffer)
            match_length=len(matched_buffer)

            if current_index == text_length-1:
                if current_buffer in search_buffer:
                    match_length+=1
                    literal='None'

                else:
                    literal=text[len(text)-1]
            else:
                literal=literal=text[current_index]

            token=[match_index_start_distance, match_length, literal]
            token_seq.append(token)
            i+=len(current_buffer)
            search_buffer=search_buffer+current_buffer

        else:
            token=[0, 0, text[i]]
            token_seq.append(token)
            search_buffer = search_buffer+text[i]
            i+=1
    print(token_seq)

text='ABCDEABCDEABCDEABCDA'
print(text)
lz77_compress(text, 100, 100)
print("\n\n")
