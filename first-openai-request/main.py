import openai

openai.api_key = "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"

modelList = openai.Model.list()

# Open a file for writing
with open("output.txt", "w") as file:
    # Write list of openAI models to output.txt
    file.write(str(modelList))


