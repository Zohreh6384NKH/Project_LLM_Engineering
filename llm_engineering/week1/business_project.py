import os 
from bs4 import BeautifulSoup 
from typing import List, Optional, Annotated, Dict
import json 
import requests
import ollama



class Website:
    def __init__(self, url:str):
        self.url = url
        response = requests.get(url)
        # print(f"response:{response}")
        self.body = response.content
        # print(f"self.body:{self.body}")
        soup = BeautifulSoup(self.body, "html.parser")
        # print(f"soup:{soup}")
        self.title = soup.title.string if soup else "no title found"
        print(f"self.title:{self.title}")
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                # print(f"irrelevant:{irrelevant}")  # Print the value of irrelevant)
                irrelevant.decompose()
                # print(f"irrelevant:{irrelevant}")
            self.text = soup.body.get_text(separator='/n', strip=True)
            print(f"self.text:{self.text}")  # Print the value of self.text)
        else:
            self.text = ""
        links = [link.get("href") for link in soup.find_all("a")]
        # print(f"soup.find_all('a'):{soup.find_all('a')}")
        # print(f"links:{links}")
        self.link = [link for link in links if link]
        
    def get_content(self, ):
        return f"webpage title:\n{self.title}\n webpage text:\n{self.text}\n "
    
    
my_website = Website("https://edwarddonner.com/")
content = my_website.get_content()
# print(f"link:{my_website.link}")  # Print the value of my_website.link
# print(f"content:{content}")



#now it turns to calling llama3 locally with ollama to figure out which links are relevant, and repalce links like "/about" with "http://company.come/about"
# we will use one shot prompting in which we provide an example of how the output should look like

link_system_prompt = "you are provided with a list of links found on a webpage.\
you are able to decide which of the links are most relevant to include in a brochure about the company,\
such as link to an about page, or the company page or Careers/Job page.\n"
link_system_prompt += "You should respond in JSON as in this example:"
link_system_prompt +="""
                        {
                            "links":[
                            {"type":"about page", "url":"https://full.url/goes/here/about"},
                            {"type":"career page", "url":"https://another/full.url/careers"}
                            ]
                        }

"""
print(f"link_system_prompt:{link_system_prompt}")  

def get_links_user_prompt(website):
    user_prompt = f"here is the list of the links on the website of {website.url}" 
    user_prompt += "please decide which of the links are relevant to web links for a brosucher about the company\
respond with the full http URL. Do not include terms of service, privacy policy, or email links.\n"
    user_prompt += "Links:\n"
    user_prompt += "\n".join(website.link)
    return user_prompt
contents_links = get_links_user_prompt(my_website)
print(f"contents_links:{contents_links}")


#with ollama.chat
def get_links(url):
    print("function started")
    
# now we want get relevant links with interacting with llm
    config_list = [{
        "model":"llama3.2",
        "api_type":"ollama",
        "client_host":"http://localhost:11434",
    }] 

    llm_config = {
        "config_list":config_list,
        "request_timeout":600,
        "temperature":0,
        "seed":43,
        "cache_seed":None
    } 

    response = ollama.chat(model="llama3.2",
                           
                        messages = [{"role":"system", "content":link_system_prompt},
                                    {"role":"user", "content":get_links_user_prompt(my_website)}],
                        
                )
    assistant_response = response["message"]["content"]
    return assistant_response
    

relevant_link = get_links("https://edwarddonner.com/")
print(f"relevant_link:{relevant_link}")



#with requests.post

ollama_api = "http://localhost:11434/api/chat"
headers = {'Content-Type': 'application/json'}
model = "llama3.2"


pay_load = {
    "model":"llama3.2",
    "messages":[{
        "role":"system", "content":link_system_prompt},
        {"role":"user", "content":get_links_user_prompt(my_website)}],
    "stream":False
}



response = requests.post(ollama_api, json=pay_load, headers=headers)
response = response.json()['message']['content']
print(f"response:{response}")
                       