# # # we are going to write a program which is going to be able to look at any webpage on the internet, scrape the content of web page and then summarise.
# # #think of it like you are building your own little web browser then summarising that web browser.
import requests
from bs4 import BeautifulSoup
import json
import ollama


    

# # import requests

# class WikipediaPage:
#     """
#     A class to fetch and store the summary of a Wikipedia article.
#     """

#     def __init__(self, title: str):
#         # Wikipedia API URL
#         url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
#         headers = {"User-Agent": "Mozilla/5.0"}  # Avoid getting blocked
        
#         response = requests.get(url, headers=headers)

#         if response.status_code == 200:  # Check if request was successful
#             data = response.json()  # Parse JSON response
#             self.title = data.get("title", "No title found")
#             self.summary = data.get("extract", "No summary available.")
#         else:
#             self.title = title
#             self.summary = "Failed to fetch page."

# # Example usage
# website = WikipediaPage("Michael Jackson")  # Replace with any topic
# website = WikipediaPage("Taylor Swift")
# # print(f"Title: {website.title}\n")
# # print(f"Summary: {website.summary}")    

# system_prompt = "You are an assistant that analyses the content of a website\
# and returns a short summary\
# ignoring the text that navigating the website.\
# respond in markdown format"

# def use_prompt_for(website):
#     user_prompt = f"you are looking at website title:{website.title}:"
#     user_prompt += "\nthe content of this website is as follows;\
# please provide a short summary from the website\n\n"
    
#     user_prompt += website.summary
#     return user_prompt
# result = use_prompt_for(website)
# print(result)


  

# def message_for(website):
#     return [{
#         "role": "user", "content": use_prompt_for(website)
#     },
#     {
#         "role": "system", "content": system_prompt 
#     }  
#     ] 
# final_result = message_for(website)
# print(final_result)









# messages = [
#         {
#             "role": "user", "content": use_prompt_for(website)
#         },
#         {
#             "role": "system", "content": system_prompt 
#         }
#     ]


# config_list = [
#     {
#         "model": "llama3.2",
#         "client_host": "http://localhost:11434",
#         "api_key": "ollama"
#     }
# ]

 
# llm_config = {
#     "request_timeout": 60,
#     "config_list": config_list,
#     "temperature": 0,
#     "seed": 43,
#     "cache": True}      # type: ignore

# def chat_with_llama3(messages):
#     """
#     send a list of messages to llama3 via ollama and return the response
#     param message: list of dictionaries containing conversation history
#     return:response from the model as string
    
#     """
#     print("function stated")
    
    
    
#     ollama_url = llm_config["config_list"][0]["client_host"] + "/api/chat"
#     model_name = llm_config["config_list"][0]["model"]
#     request_timeout = llm_config["request_timeout"]
    
#     payload = {
#         "model": model_name,
#         "messages": messages,
#         "temperature": llm_config["temperature"],
#         "seed": llm_config["seed"],
#         "request_timeout": request_timeout
#     }
#     try:
#         response = requests.post(ollama_url, json=payload, timeout=request_timeout)
#         response.raise_for_status()  #raise an error if request fails
        
#         response_json = response.json()
#         assistant_message = response_json.get("message", {}).get("content", "no response recieved")
#         return assistant_message
    
    
#     except requests.exceptions.RequestException as e:
#         return f"Request failed: {e}"
#     except json.JSONDecodeError as e:
#         return f"JSON Decode Error: {e}"
        

# # call the function to get the summary   
# # 
# result= chat_with_llama3(messages)
# print(f"result:{result}")
    
    
    
    
    
    
    

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

        # Extract assistant's response
        assistant_message = response["message"]["content"]
        
        return assistant_message

    except Exception as e:
        return f"Error: {e}"





# Step 1: Wikipedia Scraper Class
class WikipediaPage:
    def __init__(self, title: str):
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            self.title = data.get("title", "No title found")
            self.summary = data.get("extract", "No summary available.")
        else:
            self.title = title
            self.summary = "Failed to fetch page."

# Step 2: Prepare Message for LLaMA
def prepare_messages(website):
    messages = [
        {"role": "system", "content": "You are an AI assistant that summarizes website content."},
        {"role": "user", "content": f"You are looking at the website titled '{website.title}'.\n\n"
                                    f"The content of this website is as follows:\n\n{website.summary}\n\n"
                                    f"Please provide a short summary."}
    ]
    return messages

# Step 3: Get the Summary from LLaMA
def summarize_wikipedia(title):
    website = WikipediaPage(title)  # Fetch Wikipedia summary
    messages = prepare_messages(website)  # Format messages
    return chat_with_llama3(messages)  # Call the LLaMA function

# Example Usage:
result = summarize_wikipedia("Jennifer Lopez")

print("\n🔹 Summary of the webpage:")
print(result)