import gradio as gr
import os 
import requests 
from bs4 import BeautifulSoup 
from typing import List, Optional, Dict, Annotated 
from dotenv import load_dotenv 
import openai
import google.generativeai 
import anthropic 
from openai import OpenAI

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

print(result)


def shout(text):
    return text.upper()





# demo = gr.Interface(fn=meassage_gpt, inputs="text", outputs="text").launch()
# demo = gr.Interface(fn=meassage_gpt, inputs="text", outputs="text", allow_flagging= "never").launch()

# view = gr.Interface(
#     fn=shout,
#     inputs= [gr.Textbox(label="your message", lines=6)],
#     outputs=[gr.Textbox(label="response", lines=8)],
#     allow_flagging='never'
    
# )
# view.launch()



view = gr.Interface(
    fn=meassage_gpt,
    inputs= [gr.Textbox(label="your message", lines=6)],
    outputs=[gr.Textbox(label="response", lines=8)],
    allow_flagging='never'
    
)
view.launch()




