from nltk.tokenize import sent_tokenize
from transformers import GPT2TokenizerFast

# Instainsiate tokenizer
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")


# The page_text_response is a generator object, so have to read it in as 'chunks'
# Set the max length to 2096, this has to be larger than a 'chunk" of the Wiki Page
def count_tokens(text: str) -> int:
    """count the number of tokens in a string"""
    tokenizer.model_max_length = int(2096)
    return len(tokenizer.encode(text))
    