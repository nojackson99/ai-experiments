import tiktoken
import pandas as pd
import numpy as np
import os
import sys
import openai

# Get the file path to scraped data
input_folder_path = os.path.join(os.path.dirname(__file__), 'scraped-data')
input_file_path = os.path.join(input_folder_path, 'quotesLines.csv')

# Load the cl100k_base tokenizer which is designed to work with the ada-002 model
tokenizer = tiktoken.get_encoding("cl100k_base")

# Try to read csv file, if it doesn't exist throw an error to console and end execution
try:
    with open(input_file_path, 'r') as f:
        quotes = f.read().replace('\n', ' ')
    df = pd.DataFrame({'quotes': [quotes]})
except FileNotFoundError:
    error_msg = f"Error: File not found at path {input_file_path}"
    print(error_msg, file=sys.stderr)
    sys.exit(1)

# Tokenize the text and save the number of tokens to a new column
df['n_tokens'] = df.quotes.apply(lambda x: len(tokenizer.encode(x)))

# Visualize the distribution of the number of tokens per row using a histogram
df.n_tokens.hist()

# Create embeddings from the tokenized data
df['embeddings'] = df.quotes.apply(lambda x: openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding'])

# Define file for embeddings output
output_folder_path = os.path.join(os.path.dirname(__file__), 'processed')
output_file_path = os.path.join(output_folder_path, 'embeddings.csv')

df.to_csv(output_file_path)

sys.exit(0)

