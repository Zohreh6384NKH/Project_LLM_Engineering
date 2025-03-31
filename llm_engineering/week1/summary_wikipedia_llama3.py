# # # we are going to write a program which is going to be able to look at any webpage on the internet, scrape the content of web page and then summarise.
# # #think of it like you are building your own little web browser then summarising that web browser.
import requests
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