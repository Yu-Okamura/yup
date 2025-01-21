from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
# or if you trained a custom tokenizer with Hugging Face Tokenizers
# tokenizer = ByteLevelBPETokenizer("vocab.json", "merges.txt")

text = "私の名前は岡村。Yokokimthurston is a collaborative album by Yoko Ono, Kim Gordon and Thurston Moore, released by Chimera Music on 25 September 2012."
encoded_input = tokenizer.encode(text, add_special_tokens=True)
print(encoded_input)

tokens = tokenizer.convert_ids_to_tokens(encoded_input)
print(tokens)
