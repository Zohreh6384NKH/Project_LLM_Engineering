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


# a very generic system message 
system_message = "You are a helpful assistant."
def meassage_gpt(prompt):
    messages = [
        {"role":"system","content":system_message},
        {"role":"user", "content":prompt}
    ]
    response = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages
    )
    result = response.choices[0].message.content
    return result


result = meassage_gpt("how was your day today?")
result = meassage_gpt("what is the date of today?")
# print(result)





def shout(text):
    return text.upper()

demo = gr.Interface(fn=meassage_gpt, inputs="text", outputs="text").launch()
demo = gr.Interface(fn=meassage_gpt, inputs="text", outputs="text", allow_flagging= "never").launch()







# # demo with shout function
view = gr.Interface(
    fn=shout,
    inputs= [gr.Textbox(label="your message", lines=6)],
    outputs=[gr.Textbox(label="response", lines=8)],
    allow_flagging='never'
)

view.launch()



# # demo with message_gpt function
view = gr.Interface(
    fn=meassage_gpt,
    inputs= [gr.Textbox(label="your message", lines=6)],
    outputs=[gr.Textbox(label="response", lines=8)],
    allow_flagging='never'
    
)
view.launch()








# system_message = "You are a helpful assistant."
# #streaming in gradio with gpt4
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
        return result
        


view = gr.Interface(
    fn=stream_gpt,
    input=gr.Textbox(label="message", lines=6),
    outputs=gr.Textbox(label="response", lines=8),
    allow_flagging = 'never'
)
view.launch()
    
    













#building gradio with llama3.2 locally with ollama  we dont need system_message.thats why the previous code wont work

def llama_response(prompt):
    messages = [
        {"role": "user", "content": prompt}
    ]
    response = ollama.chat(model="llama3.2", messages=messages)
    return response["message"]["content"]

view = gr.Interface(
    fn=llama_response,
    inputs=gr.Textbox(label="Your message", lines=6),
    outputs=gr.Textbox(label="Response", lines=8),
    flagging_mode="never"  # updated to avoid warning
)

view.launch()







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
        yield content
        
        
        
    

view = gr.Interface(
    fn=stream_llama,
    inputs=gr.Textbox(label="Your message", lines=6),
    outputs=gr.Textbox(label="Response", lines=8),
    flagging_mode="never"  # updated to avoid warning
)

view.launch()
