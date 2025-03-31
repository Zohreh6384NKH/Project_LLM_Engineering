from IPython.display import Markdown, display
import requests 
from bs4 import BeautifulSoup 
import json
import ollama 


# config_list = [{
#     "model": "llama3",
#     "api_type": "ollama",
#     "client_host": "http://localhost:11434",  #ollama runs on this port
    
# }]



# llm_config = {"config_list": config_list,
#               "request_timeout": 600,
#               'seed': 43,
#               'temperature': 0.0,
#               }





ollama_api = "http://localhost:11434/api/chat"
headers = {'Content-Type': 'application/json'}
model = "llama3.2"



messages = [{
    "role":"user",
    "content":"Describe some of business applications of generative AI."
}]


payload = {
    "model": "llama3.2",
    "messages": messages,
    "stream": False
}





#one way to chat with llama3 is to use ollama.chat

response = ollama.chat(
    model="llama3.2",  # Use your model version
    messages=messages
)
response = response["message"]["content"]




#another way to chat with llama3 is to use ollama.post

response = requests.post(ollama_api, json=payload, headers=headers)
response = response.json()["message"]["content"]   
print(f"response: {response}")
