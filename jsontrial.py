import json
import time

# Define the text to be stored in the JSON file
text = "You ~ "+"Hello, world!"

# Define the filename for the JSON file
filename = "text.json"

with open(filename, "r") as f:
    data = json.load(f)
    print(data)

# Dump the text to a JSON file
with open(filename, "w") as f:
    json.dump(text, f)
