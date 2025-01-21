def lz77_compress(data: str, window_size: int, max_length: int):
    """
    Compress a UTF-8 string using LZ77.

    :param data: The input string (UTF-8) to compress.
    :param window_size: The size of the sliding window (in characters).
    :param max_length: The maximum match length to search for (in characters).
    :return: A list of tokens (offset, length, next_char), containing
             the compressed representation and all information needed
             for decompression.
    """
    i = 0
    output_tokens = []
    data_length = len(data)

    while i < data_length:
        best_length = 0
        best_offset = 0

        search_window_start = max(0, i - window_size)

        for j in range(search_window_start, i):
            match_length = 0

            while (match_length < max_length
                   and i + match_length < data_length
                   and data[j + match_length] == data[i + match_length]):
                match_length += 1

            if match_length > best_length:
                best_length = match_length
                best_offset = i - j

        if best_length > 0:
            next_char_index = i + best_length
            next_char = data[next_char_index] if next_char_index < data_length else ''
            output_tokens.append((best_offset, best_length, next_char))
            i += best_length + 1
        else:
            output_tokens.append((0, 0, data[i]))
            i += 1

    return output_tokens


def lz77_decompress(tokens):
    """
    Decompress a list of LZ77 tokens back into the original string.

    Each token should be (offset, length, next_char):
      - offset: how far back to look for a match
      - length: how many characters matched
      - next_char: the next literal character (or '' if we are at the end)
    """
    output_chars = []

    for offset, length, next_char in tokens:
        if offset == 0 and length == 0:
            # Literal character, just append
            output_chars.append(next_char)
        else:
            # We have a back-reference:
            # offset tells us how far back to go,
            # length tells us how many characters to copy
            start_index = len(output_chars) - offset
            for i in range(length):
                output_chars.append(output_chars[start_index + i])
            if next_char:  # If next_char is not empty, append it
                output_chars.append(next_char)

    return "".join(output_chars)


if __name__ == "__main__":
    # Example usage:
    input_str = "ABABABAABABA"
    window_size = 6
    max_match_length = 4

    # Compress
    tokens = lz77_compress(input_str, window_size, max_match_length)
    print("Tokens:", tokens)

    # Decompress
    decompressed = lz77_decompress(tokens)
    print("Decompressed:", decompressed)
    print("Matches original?", decompressed == input_str)
