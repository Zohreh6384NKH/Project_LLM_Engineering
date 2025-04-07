import os 
import json 
from dotenv import load_dotenv 
from openai import OpenAI
import gradio as gr 


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model="gpt-4o-mini"
openai = OpenAI()

system_message = "You are a helpful assistant for an Ailline called FlightAI"
system_message += "give short, courteous answer no more than 1 sentense"
system_message += "Always be accurate, if you dont know the answer, say so"

def chat(message, history):
    messages = [{"role":"user", "content":system_message}]
    for user_message, assistant_message in history:
        messages.append({"role":"user", "content":user_message})
        messages.append({"role":"assistant", "content":assistant_message})
    messages.append({"role":"user", "content":message})
    response = openai.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content

    # stream = openai.chat.completions.create(model=model, messages=messages)
    # response=''
    # for chunk in response:
    #     response += chunk.choices[0].delta.content or ''
    #     yield response
        
# view = gr.ChatInterface(fn=chat).launch()


#lets make a useful function

# ticket_prices = {"london":"799$", "berlin":"499$", "paris":"899$", "tokyo":"1400$"}
# def get_ticket_price(destination_city):
#     print(f"tool get ticket price called for {destination_city}")
#     city = destination_city.lower()
#     return ticket_prices.get(city, "unknown")
# print(get_ticket_price("Berlin"))



