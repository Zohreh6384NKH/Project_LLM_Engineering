import autogen
from autogen import UserProxyAgent, AssistantAgent, config_list_from_json, GroupChat, GroupChatManager, ConversableAgent
from typing import Annotated
import os
import requests
import base64
import json
import chardet




# Load configuration for agents
 

config_list = [
    {
        "model": "llama3.1",
        "api_key": "ollama_manu",
        "cache_seed": None,
        "base_url": "http://localhost:11434/v1",
        "timeout": 60,
    }
]
llm_config = {"config_list": config_list}

# Define the agents
# cloner_agent = AssistantAgent(
#     name="cloner_agent",
#     system_message="You clone the github repository to a given directory.",
#     llm_config=llm_config,
# )

file_listing_agent = AssistantAgent(
    name="file_listing_agent",
    #system_message="You execute the list_files function.",
    llm_config=llm_config,
)

fetch_and_summarize_agent = AssistantAgent(
    name="fetch_and_summarize_agent",
    #system_message="You execute the fetch_file_content function.",
    llm_config=llm_config,
)

summarizer_agent = AssistantAgent(
    name="summarizer_agent",
    #system_message="You execute the summarize_content function.",
    llm_config=llm_config,
)

UserProxy = ConversableAgent(
    name="UserProxy",
    llm_config=llm_config,
    human_input_mode="NEVER",
    max_consecutive_auto_reply=2,
    code_execution_config=False,
)


# Define the functions to be executed by agents
# @UserProxy.register_for_execution()
# @cloner_agent.register_for_llm(description="Clone a GitHub repository to a local directory.")
# def clone_repo(repo_url: Annotated[str, "The URL of the GitHub repository"], repo_dir: Annotated[str, "The Local Directory of the GitHub repository"]) -> str:
#     os.system(f"git clone {repo_url} {repo_dir}")
#     return repo_dir


# @file_listing_agent.register_for_execution()
@UserProxy.register_for_execution()
@file_listing_agent.register_for_llm(description="List all files in a local directory.")
def list_files(repo_dir: Annotated[str, "The Local Directory"]) -> list:
    files = []
    files_list = os.listdir(repo_dir)
    for file in files_list:
        if os.path.isfile(os.path.join(repo_dir, file)):
            files.append(os.path.join(repo_dir, file))
        elif os.path.isdir(os.path.join(repo_dir, file)):
            nested_files = list_files(os.path.join(repo_dir, file))
            if isinstance(nested_files, list):
                files.extend(nested_files)
    return files



# @content_fetcher_agent.register_for_execution()
# @UserProxy.register_for_execution()
# @content_fetcher_agent.register_for_llm(description="Fetch content of files from a local GitHub repository.")
# def fetch_file_content(files_list: Annotated[list, "List of file paths"]) -> dict:
#     contents = {}
#     for file_path in files_list:
#         with open(file_path, "rb") as f:
#             tmp_content = f.read()
#             encode_result = chardet.detect(tmp_content)
            
#             if encode_result["encoding"] != None: #and encode_result["encoding"] != "Windows-1254":
#                 try:
#                     contents[file_path] = tmp_content.decode(encode_result["encoding"])
#                 except:
#                     contents[file_path] = tmp_content.decode('latin-1')
#             else:
#                 contents[file_path] = tmp_content
#     return contents





# @summarizer_agent.register_for_execution()
@UserProxy.register_for_execution()
@fetch_and_summarize_agent.register_for_llm(name="fands", description="Summarize the contents of files listed from a directory.")
def summarize_content(
    files_list: Annotated[list, "List of file paths"]) -> dict[str, str]:
    
    contents = {}
    for file_path in files_list:
        with open(file_path, "rb") as f:
            tmp_content = f.read()
            encode_result = chardet.detect(tmp_content)
            
            if encode_result["encoding"] != None: #and encode_result["encoding"] != "Windows-1254":
                try:
                    contents[file_path] = tmp_content.decode(encode_result["encoding"])
                except:
                    contents[file_path] = tmp_content.decode('latin-1')
            else:
                contents[file_path] = tmp_content

    summaries = {}
    for file_name, content in contents.items():
        if isinstance(content, str):  # Ensure content is a valid string
            try:
                # Create a summarization prompt
                prompt = (
                    f"Summarize the following content of the file '{file_name}' in 3 concise sentences:\n\n"
                    f"{content}"
                )

                # Call the summarizer agent to generate the summary
                llm_response = summarizer_agent.generate_reply(messages=[{"role": "user", "content": prompt}])

                # Check if the response is valid and contains the expected content
                if isinstance(llm_response, dict) and "content" in llm_response:
                    summaries[file_name] = llm_response["content"]
                else:
                    summaries[file_name] = f"Unexpected response format: {llm_response}"
            except Exception as e:
                summaries[file_name] = f"Error summarizing content: {str(e)}"
        else:
            summaries[file_name] = "Invalid content format or failed to fetch."
    return summaries


groupchat = GroupChat(agents=[UserProxy, file_listing_agent, fetch_and_summarize_agent], messages=[], speaker_selection_method='round_robin', max_round=12) # cloner_agent, #UserProxy, # file_listing_agent # , speaker_selection_method='round_robin'

manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# input_url = input("Enter the URL of the GitHub repository: ")
input_dir = "/home/nima/workspace/clone_git/AutoGwn_tutorial"#input("Enter the Local Directory of the GitHub repository (please use absolute path): ")
# Please clone the repository: {input_url}, to the local directory: {input_dir} using cloner_agent.
UserProxy.initiate_chats(
    [
        {
            "recipient": manager,
            "message": f"Follow the following pipeline: 1) First call file_listing_agent which lists all files in the repository: {input_dir}, then pass the results as an argument to fands function. \
            2) UserProxy and fetch_and_summarize_agent will fetch the content of the files returned in the previous step, ask from chat manager for the results of previous step.",
            "clear_history": False,
            "silent": False,
            "summary_method": "last_msg",
        }
        
    ]
)



