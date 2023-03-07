import openai
import os
from dotenv import load_dotenv

dotenv_path = '~/.env'
load_dotenv(dotenv_path)

openai_api_key = os.getenv("OPENAI_API_KEY")
print(openai_api_key)
openai.api_key = openai_api_key

# modelList = openai.Model.list()

# # Open a file for writing
# with open("output.txt", "w") as file:
#     # Write list of openAI models to output.txt
#     file.write(str(modelList))


