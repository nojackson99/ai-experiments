import tiktoken
import pandas as pd
import numpy as np
import os
import sys
import openai
from openai.embeddings_utils import distances_from_embeddings


def create_context(question, df, max_len=1800, size="ada"):
    """
    Create a context for a question by finding the most similar context from the dataframe
    """

    # Get the embeddings for the question
    q_embeddings = openai.Embedding.create(input=question, engine='text-embedding-ada-002')['data'][0]['embedding']

    # Get the distances from the embeddings
    df['distances'] = distances_from_embeddings(q_embeddings, df['embeddings'].values, distance_metric='cosine')

    returns = []
    cur_len = 0

    # Sort by distance and add the text to the context until the context is too long
    for i, row in df.sort_values('distances', ascending=True).iterrows():
        
        # Add the length of the text to the current length
        cur_len += row['n_tokens'] + 4
        
        # If the context is too long, break
        if cur_len > max_len:
            break
        
        # Else add it to the text that is being returned
        returns.append(row["quotes"])

    # Return the context
    return "\n\n###\n\n".join(returns)

def answer_question(
    df,
    question,
    model="text-davinci-003",
    max_len=1800,
    size="ada",
    debug=False,
    max_tokens=150,
    stop_sequence=None
):
    """
    Answer a question based on the most similar context from the dataframe texts
    """
    context = create_context(
        question,
        df,
        max_len=max_len,
        size=size,
    )
    # If debug, print the raw model response
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        # Create a completions using the question and context
        response = openai.Completion.create(
            prompt=f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_sequence,
            model=model,
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        print(e)
        return ""

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

#df.to_csv(output_file_path)

# print(df['embeddings'])
# Convert embeddings to numpy array
# df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)
df['embeddings'] = df['embeddings']

df.head()

answer = answer_question(df, question="Can you tell me a quote that is attributed by albert einstein")
print(answer)

answer = answer_question(df, question="What tags are associated with the quote by Jane Austen?", debug=False)
print(answer)

answer = answer_question(df, question="What is ChatGPT?", debug=False)
print(answer)

sys.exit(0)

