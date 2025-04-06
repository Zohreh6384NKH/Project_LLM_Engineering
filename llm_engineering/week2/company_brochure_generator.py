import gradio as gr
import os 
import requests 
from bs4 import BeautifulSoup 
from typing import List, Optional, Dict, Annotated 
from dotenv import load_dotenv 
import openai
from openai import OpenAI
import ollama


class Website:
    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.body = response.content
        soup = BeautifulSoup(self.body, 'html.parser')
        self.title = soup.title.string if soup.title else  "no title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
    
    def get_content(self):
        return f"Webpage title:\n{self.title}\nWebpage content:\n{self.text}\n\n"
    
    
    






load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")





system_message = "You are an assistant that analyses the content of a company website landing page.\
and creates a short brochure about the company for prospective customers, investors and recruits. respond in markdown"
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



def stream_brochure(company_name, url, model):
    prompt = f"please generate company brochure for the company {company_name} here is the landing page:\n"
    prompt += Website(url).get_content()
    if model=="gpt-4o-mini":
        result == stream_gpt(prompt)
    elif model == "llama3.2":
        result = stream_llama(prompt)
    
    else:
        raise ValueError(f"Unknown model: {model}")
    for chunk in result:
        yield chunk
        
        
        
    
view = gr.Interface(
    fn=stream_brochure,
    inputs = [
            gr.Textbox(label="Company name:"),
            gr.Textbox(label="landing page url:"),
            gr.Dropdown(["gpt-4o-mini", "llama3.2"], label="select model")],
    outputs = [gr.Markdown(label="Brochure:")],
    flagging_mode="never"
)
view.launch()
    
    

