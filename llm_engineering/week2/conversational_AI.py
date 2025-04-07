import os 
from dotenv import load_dotenv 
from openai import OpenAI 
import gradio as gr 
import openai


#load environment variable from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


system_message = "you are a helpful assistant in a clothes store. you should try to gently encourage \
the customers to try the items thar are on sale, forexample if the customer says Im looking to buy a hat,\
you could reply somthing like  wonderful- we have lots of hats-including several hats that are part of our \
sale event, 60% off today only."


#reminder of the structure of prompt message to openai 
def chat(message, history):
    
    messages = [{"role":"system", "content":system_message}]
    for user_message, assistant_message in history:
        messages.append({"role":"user", "content":"user_message"})
        messages.append({"role":"assistant", "content": "assistant_message"})
    messages.append({"role":"user", "content":message})
    print(f"history is:\n")
    print(history)
    print(f"messages is:\n")
    print(messages)
    
    stream = openai.chat.completions.create(
        model = "gpt-4o-mini", messages = messages, stream = True
    )
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response
        
view = gr.ChatInterface(fn=chat).launch()  #we want to build chat style interface so we need to use chatinterface