# # import requests
import requests
import os
# from Ipython.display import Markdown, display
from bs4 import BeautifulSoup
import json
import ollama




def chat_with_llama3(messages):
    """
    Sends a conversation to LLaMA 3 via Ollama and returns the response.

    :param messages: List of dictionaries containing conversation history.
    :return: Response from the model as a string.
    """
    print("Function started...")

    try:
        # Send message to Ollama
        response = ollama.chat(
            model="llama3.2",  # Use your model version
            messages=messages
        )
        print(f"Response: {response}")

        # Extract assistant's response
        assistant_message = response["message"]["content"]
        print(f"Message from assistant: {assistant_message}")
        
        return assistant_message

    except Exception as e:
        return f"Error: {e}"




class Website:
    """
    A class to represent a waeb page.
    """
    
    url:str
    title:str
    text:str

    def __init__(self, url: str):
        
        self.url = url
        response = requests.get(url)  #fetches  webpage HTML
        # print(f"response:{response}")  
        soup = BeautifulSoup(response.content, "html.parser")   # parses HTML using BeautifulSoup
        # print(f"soup:{soup}")
        self.title = soup.title.string if soup.title else "No title found"   # extract webpage title
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()   #removes unwanted elements
        self.text = soup.body.get_text(separator="\n", strip=True)   #extract clean webpage text

        

# Example usage
ed = Website("https://edwarddonner.com/")  # Replace with any topic
# ed = Website("https://en.wikipedia.org/wiki/Cristiano_Ronaldo") 

# print(f"Title: {ed.title}\n")
# print(f"text: {ed.text}") 

system_prompt = "you are an asistant that analyses the content of a website\
and provide a short summary ignoring the text that might be navigation related\
respond in markdown"


def prepare_messages(website):
    messages = [
        {"role": "system", "content": "You are an AI assistant that summarizes website content."},
        {"role": "user", "content": f"You are looking at the website titled '{website.title}'.\n\n"
                                    f"The content of this website is as follows:\n\n{website.text}\n\n"
                                    f"Please provide a short summary."}
    ]
    return messages

messages = prepare_messages(ed)


def summarise(url):
    print("function starts")
    website = Website(url)
    messages = prepare_messages(website)
    return chat_with_llama3(messages)
    
    
url = "https://edwarddonner.com/"   
summary = summarise(url)
print(f"summary of page:{summary}")
        
    
    
    
    



  

