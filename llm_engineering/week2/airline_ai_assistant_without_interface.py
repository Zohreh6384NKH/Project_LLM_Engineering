import os 
import json 
import openai
from dotenv import load_dotenv 
from openai import OpenAI
import gradio as gr 

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model  = "gpt-4o-mini"


system_message = "you are a helpful assistant for an Airline call FlightAI"
system_message += "give short, courteous answer no more than 1 sentense"
system_message += "Always be accurate, if you dont know the answer, say so"



# Load environment variables and set up OpenAI client
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model = "gpt-4o-mini"
openai = OpenAI()

# System instructions for the assistant
system_message = "You are a helpful assistant for an airline called FlightAI. "
system_message += "Give short, courteous answers no more than 1 sentence. "
system_message += "Always be accurate; if you don't know the answer, say so."

# Ticket price lookup
ticket_prices = {"london": "799$", "berlin": "499$", "paris": "899$", "tokyo": "1400$"}

def get_ticket_price(destination_city):
    print(f"Tool 'get_ticket_price' called for: {destination_city}")
    city = destination_city.lower()
    return ticket_prices.get(city, "unknown")

# Tool definition for OpenAI function calling
price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}
tools = [{"type": "function", "function": price_function}]

# Tool handler
def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    city = arguments.get("destination_city")
    price = get_ticket_price(city)
    response = {
        "role": "tool",
        "content": json.dumps({"destination_city": city, "price": price}),
        "tool_call_id": tool_call.id
    }
    print(f"response is:\n")
    print(response)
    return response, city

# Main chat function
def chat(message, history):
    messages = [{"role": "system", "content": system_message}]
    for human, assistant in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assistant})
    messages.append({"role": "user", "content": message})
    print(f"messages is:\n")
    print(messages)
    
    response = openai.chat.completions.create(model=model, messages=messages, tools=tools)
    print(f"response is:\n")
    print(response)
    
    if response.choices[0].finish_reason == "tool_calls":
        
        message = response.choices[0].message
        print(f"message is:\n")
        print(message)
        tool_response, city = handle_tool_call(message)
        messages.append(message)
        messages.append(tool_response)
        print(f"messages2 is:\n")
        print(messages)
        
        
        # Final assistant response after tool use
        response = openai.chat.completions.create(model=model, messages=messages)
    
    return response.choices[0].message.content

# Simple CLI loop
if __name__ == "__main__":
    
    print("Welcome to FlightAI! Ask me about ticket prices or travel destinations. (Type 'exit' to quit)\n")
    
    chat_history = []
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            break
        reply = chat(user_input, chat_history)
        print(f"reply:{reply}")
        chat_history.append((user_input, reply))
        print(f"chat_history:{chat_history}")
        print("FlightAI:", reply)
