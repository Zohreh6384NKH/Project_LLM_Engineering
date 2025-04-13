import os 
import torch
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer, BitsAndBytesConfig 
from huggingface_hub import login


load_dotenv()
huggingface_token = os.getenv("HUGGINGFACE_TOKEN")

#instruct models
LLAMA = "meta-llama/Llama-3.1-8B-Instruct"
PHI3 = "microsoft/Phi-3-mini-4k-instruct"
GEMMA2 = "google/gemma-2-2b-it"
QWEN2 = "Qwen/Qwen2-7B-Instruct"
# MIXTRAL = "Mistral/Mixtral-8x7B-Instruct-v0.1"


login(token=huggingface_token, add_to_git_credential=True)
tokenizer = AutoTokenizer.from_pretrained(PHI3, trust_remote_code=True)

text = "hello there how are you?"
token = tokenizer.encode(text)
# print(f"token for phi3:{token}")



login(token=huggingface_token, add_to_git_credential=True)
tokenizer = AutoTokenizer.from_pretrained(GEMMA2, trust_remote_code=True)

text = "hello there how are you?"
token = tokenizer.encode(text)
# print(f"token for gemma:{token}")


login(token=huggingface_token, add_to_git_credential=True)
tokenizer = AutoTokenizer.from_pretrained(QWEN2, trust_remote_code=True)

text = "hello there how are you?"
token = tokenizer.encode(text)
# print(f"token for qwen:{token}")

messages = [
    {"role":"system", "content":"you are a helpful assistant"},
    {"role":"user", "content":"tell me a light-heartened jok for the room of data scientists "}
]



# login(token=huggingface_token, add_to_git_credential=True)
# tokenizer = AutoTokenizer.from_pretrained(MIXTRAL, trust_remote_code=True)

# text = "hello there how are you?"
# token = tokenizer.encode(text)
# print(f"token for mixtral:{token}")




# quantization config- this allows us to load the model into memory and use less memory
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

#tokenizer
tokenizer = AutoTokenizer.from_pretrained(LLAMA, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")



#the model
model = AutoModelForCausalLM.from_pretrained(
    LLAMA,
    quantization_config=quant_config,
    device_map="auto",
)

# memory = model.get_memory_footprint() / 1e6
# print(f"memory usage:{memory:.1f} MB")

output = model.generate(inputs, max_new_tokens=100)
print(tokenizer.decode(output[0]))

# clean up
del model
del tokenizer
del inputs, output

# Empty CUDA cache if you used GPU
torch.cuda.empty_cache()


#wrapping everything to a function and add streaming
def generate(model, messages):
    tokenizer = AutoTokenizer.from_pretrained(model, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cuda")
    model = AutoModelForCausalLM.from_pretrained(model, quantization_config=quant_config, device_map="auto")
    streamer = TextStreamer(tokenizer)
    output = model.generate(inputs, max_new_tokens=80, streamer=streamer)
    
generate(LLAMA, messages)











