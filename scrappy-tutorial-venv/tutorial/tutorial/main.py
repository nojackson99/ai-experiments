import tiktoken
import pandas as pd
import os
import sys
import openai

# Get the file path to scraped data
folder_path = os.path.join(os.path.dirname(__file__), 'scraped-data')
file_path = os.path.join(folder_path, 'quotesLines.csv')

# Load the cl100k_base tokenizer which is designed to work with the ada-002 model
tokenizer = tiktoken.get_encoding("cl100k_base")

# Try to read csv file, if it doesn't exist throw an error to console and end execution
try:
    df = pd.read_csv(file_path, header=None)
except FileNotFoundError:
    error_msg = f"Error: File not found at path {file_path}"
    print(error_msg, file=sys.stderr)
    sys.exit(1)

# Add a new column to the DataFrame with the line number
df.insert(0, 'line_number', range(1, len(df)+1))

# Rename the columns of the DataFrame
df.columns = ['line_number', 'text']

# Tokenize the text and save the number of tokens to a new column
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

# Visualize the distribution of the number of tokens per row using a histogram
df.n_tokens.hist()

# Create embeddings from the tokenized data
df['embeddings'] = df.text.apply(lambda x: openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding'])

df.to_csv('processed/embeddings.csv')
df.head()

sys.exit(0)

