def convert_to_binary(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        f_origin = f.read()
    # Convert to UTF-8 bytes
    f_utf8 = f_origin.encode('utf-8')
    # Convert each byte to a binary string, grouped into 4-bit chunks
    f_binary = ''.join(format(byte, '08b') for byte in f_utf8)
    # Group into 4-bit patterns
    f_4bit_patterns = [f_binary[i:i+8] for i in range(0, len(f_binary), 8)]
    print('4-bit patterns:', f_4bit_patterns)
    print('Number of 4-bit patterns:', len(f_4bit_patterns))
    return f_4bit_patterns

def find_longest_match(data, current_index, window_size):
    """
    Finds the longest match to a substring starting at current_index within the sliding window.

    :param data: List of 4-bit patterns as strings.
    :param current_index: The current position in the data.
    :param window_size: The maximum size of the sliding window.
    :return: (offset, length) of the longest match.
    """
    search_start = max(0, current_index - window_size)
    search_window = data[search_start:current_index]

    longest_match_length = 0
    longest_match_offset = 0

    # Check substrings starting at each position in the search window
    for i in range(len(search_window)):
        match_length = 0

        # Compare patterns in the search window with the lookahead buffer
        while (current_index + match_length < len(data) and
               i + match_length < len(search_window) and
               search_window[i + match_length] == data[current_index + match_length]):
            match_length += 1

        # Update longest match if necessary
        if match_length > longest_match_length:
            longest_match_length = match_length
            longest_match_offset = len(search_window) - i

    return longest_match_offset, longest_match_length

def lz77_compress(data, window_size=1024):
    """
    LZ77 compression algorithm.

    :param data: List of 4-bit patterns as strings.
    :param window_size: Max distance to look back in the sliding window.
    :return: List of tokens (offset, length, next_pattern).
    """
    i = 0
    compressed_output = []

    while i < len(data):
        # Find the longest match in the sliding window
        match_offset, match_length = find_longest_match(data, i, window_size)

        if match_length > 0:
            # Get the next pattern after the match, if it exists
            next_pattern_index = i + match_length
            next_pattern = data[next_pattern_index] if next_pattern_index < len(data) else None

            # Add match token
            compressed_output.append((match_offset, match_length, next_pattern))

            # Move pointer forward
            i += match_length + 1
        else:
            # Add literal token
            compressed_output.append((0, 0, data[i]))
            i += 1

    print('Compressed Output:', compressed_output)
    return compressed_output

# Example Usage
print('\n\n\n')
compressed_output = lz77_compress(convert_to_binary('content.txt'))
