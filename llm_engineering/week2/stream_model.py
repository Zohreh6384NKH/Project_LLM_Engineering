import gradio as gr
import os 
import requests 
from bs4 import BeautifulSoup 
from typing import List, Optional, Dict, Annotated 
from dotenv import load_dotenv 
import openai
from openai import OpenAI
import ollama







load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")





system_message = "You are a helpful assistant."
#streaming in gradio with gpt4
def stream_gpt(prompt):
    messages=[
        {"role":"user", "content":prompt},
        {"role":"system", "content":system_message}
    ]
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in response:
        result +=chunk.choices[0].delta.content or ""
        yield result   #yield is used to stream the response/ yield progressively
        


view = gr.Interface(
    fn=stream_gpt,
    inputs=gr.Textbox(label="message", lines=6),
    outputs=gr.Textbox(label="response", lines=8),
    allow_flagging = 'never'
)
# view.launch()
    
    




















#now use gradio with streaming response from llama3.2 locally with ollama

def stream_llama(prompt):
    messages = [
        {"role": "user", "content": prompt}
    ]
    response = ollama.chat(model="llama3.2", messages=messages, stream=True)
    # print(response["message"]["content"])
    
    content = ""
    for chunk in response:
        content += chunk.get("message", {}).get("content", "")
        yield content    ##yield is used to stream the response/ yield progressively
        
        
        
    

view = gr.Interface(
    fn=stream_llama,
    inputs=gr.Textbox(label="Your message", lines=6),
    outputs=gr.Textbox(label="Response", lines=8),
    flagging_mode="never"  # updated to avoid warning
)

# view.launch()




def stream_model(prompt, model):
    
    if model == "gpt-4o-mini":
        result = stream_gpt(prompt)
    elif model == "llama3.2":
        result = stream_llama(prompt)
    else:
        raise ValueError(f"Unknown model: {model}")
    for chunk in result:
        yield chunk
    
view = gr.Interface(
    fn=stream_model,
    inputs = [gr.Textbox(label="your_message:"), gr.Dropdown(["gpt-4o-mini", "llama3.2"], label="select model")],
    outputs = [gr.Markdown(label="response:")],
    flagging_mode="never"
)
view.launch()
    
    

