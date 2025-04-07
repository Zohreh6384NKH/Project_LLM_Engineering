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



#lets make a useful function

ticket_prices = {"london":"799$", "berlin":"499$", "paris":"899$", "tokyo":"1400$"}
def get_ticket_price(destination_city):
    print(f"tool get ticket price called for {destination_city}")
    city = destination_city.lower()
    return ticket_prices.get(city, "unknown")
print(get_ticket_price("Berlin"))



price_function = {
    "name":"get_ticket_price",
    "description":"Get the price of a return ticket to the destination city.call this whenever you need to know the ticket price, forexample the ticket to get to the city.",
    "parameters":{
        "type":"object",
        "properties":{
            "destination_city":{
                "type":"string",
                "description":"the city that the customers wants to travel to",
        },
        
    },
    "required":["destination_city"],
    "additionalProperties":False
}
}
tools = [{"type":"function", "function": price_function}]


def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    city = arguments.get("destination_city")
    price = get_ticket_price(city)
    response = {
        "role":"tool",
        "content":json.dumps({"destination_city":city, "price":price}),
        "tool_call_id": message.tool_calls[0].id
    }
    return response, city
    
    

def chat(message, history):
    messages = [{"role":"user", "content":system_message}]
    for human, assistant in history:
        messages.append({"role":"user", "content":human})
        messages.append({"role":"assistant", "content":assistant})
    messages.append({"role":"user", "content":message})
    response = openai.chat.completions.create(model=model, messages=messages, tools=tools)
    
    if response.choices[0].finish_reason=="tool_calls":
        message = response.choices[0].message
        response, city = handle_tool_call(message)
        messages.append(message)
        messages.append(response)
        
        response = openai.chat.completions.create(model=model, messages=messages)
    
    
    return response.choices[0].message.content

view = gr.ChatInterface(fn=chat).launch()    



