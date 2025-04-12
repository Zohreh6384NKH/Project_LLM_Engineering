import transformers
import torch
from transformers import AutoTokenizer
from huggingface_hub import login
from dotenv import load_dotenv 
import os

load_dotenv()
huggingface_token = os.getenv("HUGGINGFACE_TOKEN")


login(token=huggingface_token, add_to_git_credential=True)

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B", trust_remote_code=True)  ## I dont have access to llama3.1-8B but have llama3.2-1B
text = "Hello how are you today?"
token = tokenizer.encode(text)
print(f"tokens are :\n{token}")
txt_back = tokenizer.decode(token)
print(f"text is:{txt_back}")
batch_txt_back = tokenizer.batch_decode(token)
print(f"batch text is:{batch_txt_back}")
# print(tokenizer.vocab)
# print(tokenizer.get_added_vocab())

# print(len(text))
# print(len(token))