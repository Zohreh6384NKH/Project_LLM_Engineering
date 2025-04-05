import os 
import json 
import requests 
from bs4 import BeautifulSoup 
from typing import List, Optional, Dict, Annotated 
from dotenv import load_dotenv 
import openai



load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print("api key found")
    
class Website:
    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.body = response.content
        soup = BeautifulSoup(self.body, 'html.parser')
        self.title = soup.title.string if soup.title else "title not found"
        if soup.body: 
            for irrelevant in soup.body(["script", "img", "input", "style"]):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator='\n', strip=True)
        else:
            self.text = ""
        links = [link.get('href') for link in soup.find_all('a')]
        self.links = [link for link in links if links]
    
    def get_contents(self,):
        return f" Webpage title:\n{self.title}\n Webpage text:\n{self.text}\n\n"
    


ed = Website("https://edwarddonner.com/")
contents = ed.get_contents()
print(f"links are :{ed.links}")


# anth = Website("https://anthropic.com")
# contents = anth.get_contents()
print(f"contents:{contents}")
ed_2 = Website(ed.links[2])
print(ed_2.get_contents())


# we want to use gpt-4o mini to figure out which links are relevant
link_system_prompt = "you are provided with list of links found on webpage\
you are able to decide which of the links would be the most relevant to include in the brochure about the company.\
such as links to About page, or Company page , or Career/Jobs page.\n"
link_system_prompt += "you should respond in JSON as in this example:"
link_system_prompt += """
{
    "Links":[
        {"type": "about page", "url":"full.url/goes/here/about"},
        {"type": "carrer page", "url":"another.full.url/careers"}
    ]
}

""" 
def get_links_user_prompt(website):
    
    user_prompt = f"here is the list of links on the website of {website.url}"
    user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL:\
Do not include Terms of service, Privacy, Email links.\n" 
    user_prompt += "Links:\n"
    user_prompt += "\n".join(website.links)
    return user_prompt


def get_links(url):
    website = Website(url)
    completion = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "user", "content":get_links_user_prompt(website) },
            {"role": "system", "content": link_system_prompt}
        ],
        response_format = {"type":"json_object"}
    )
    result = completion.choices[0].message.content
    return json.loads(result)

result = get_links("https://edwarddonner.com/")
print(result)
    
#now we want to get all the details from relevant link
def get_all_details(url):
    
    result = f"landing page:\n"
    result += Website(url).get_contents()
    links = get_links(url)
    print(type(links))
    print(f"found links:{links}\n")
    for link in links["Links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).get_contents()
    return result

all_details = get_all_details("https://edwarddonner.com/")
print(all_details)
    
    
    
    
    