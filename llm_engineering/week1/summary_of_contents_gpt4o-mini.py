import openai 
import os
from dotenv import load_dotenv 
from bs4 import BeautifulSoup
from openai import OpenAI
import requests



# Load environment variables from .env

load_dotenv()   #loads env. file and loads in environment
api_key = os.getenv("OPENAI_API_KEY")  #put the api key in variable called api_key


if not api_key:
    print("no api key was found")
elif api_key[:8] != "sk-proj-":
    print("an api key was found but it dosnt start with sk-proj- please check to use the right key")
else:
    print("api key was found")








# response = openai.ChatCompletion.create(
#     model="gpt-4o",
#     messages=[{"role": "system", "content": "Say 'Hello!'"}]
# )
# print(response["choices"][0]["message"]["content"])



# a class to represent a webpage
class Website:
    def __init__(self, url):
        self.url = url 
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        self.title = soup.title.string if soup.title else "no title found"
        for irrelevant in soup.body(['style', 'script', 'img', 'input']):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator='\n', strip=True)
    
    
    
ed = Website("https://edwarddonner.com")
print(ed.title)
print(ed.text)

system_prompt = "You are an asistant that analyses the contents of a website.\
and provide a short summary, ignoring the text that might be navigation related.\
respond in markdown"

def user_prompt_for(website):
    user_prompt = f"you are looking at a website titled:{website.title}"
    user_prompt += "the content of the website are as follows:\
please provide a short summary in markdown.\
if it includes news or announcement, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt

contents = user_prompt_for(ed)
print(f"contents:{contents}")


def message_for(website):
    return [
        {"role":"user", "content":user_prompt_for(website)},
        {"role": "system", "content": system_prompt}
    ]

print(message_for(ed))


def summarize(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages = message_for(website)
    )
    return response.choices[0].message.content



summary_of_contents = summarize("https://edwarddonner.com")
print(f"summary_of_contents:{summary_of_contents}")
        
        