import os
import argparse
import pprint
from dotenv import load_dotenv

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v6_0.wiki import WikiClient
import rest_azure_openai

import numpy as np
import pandas as pd
import openai

import generate_questions
import generate_answers
import generate_embeddings
import token_utils


# ADO Personal access token, ADO URL, OpenAI Key
load_dotenv()
personal_access_token = os.getenv('personal_access_token')
organization_url = os.getenv('organization_url')
wiki_page_path = os.getenv('wiki_page_path')
openai.api_key = os.getenv('public_openai_api_key')

entered_arguments = argparse.ArgumentParser()
entered_arguments.add_argument("-q", "--question", help="Enter a question realting to the Wiki Page")
args = entered_arguments.parse_args()

# Create a connection to the org
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get a client (the "core" client provides access to projects, teams, etc)
core_client = connection.clients.get_core_client()

# Get the first page of projects
get_projects_response = core_client.get_projects()
index = 0
while get_projects_response is not None:
    for project in get_projects_response.value:
        if project.name == "UC":
            pprint.pprint("ProjectName = " + project.name )
            pprint.pprint("Wiki id = " + project.id )
        index += 1
    if get_projects_response.continuation_token is not None and get_projects_response.continuation_token != "":
        # Get the next page of projects
        get_projects_response = core_client.get_projects(continuation_token=get_projects_response.continuation_token)
    else:
        # All projects have been retrieved
        get_projects_response = None

# Create a WikiCLient and then get the Page meta data and then the page text
wiki_client = WikiClient(base_url=connection.base_url, creds=connection._creds)
page = wiki_client.get_page(project="UC", wiki_identifier="UC.wiki", path=wiki_page_path)
page_data = wiki_client.get_page_data(project="UC", wiki_identifier="UC.wiki", page_id=page.page.id)
page_text_response = wiki_client.get_page_text(project="UC", wiki_identifier="UC.wiki", path=os.getenv('wiki_page_path'), include_content=True)
page_text = ""
token_count = 0
token_count_chunk = 0

# Loop though the generator object and build a string based on those chunks, and print it out
# get token count for the string
for chunk in page_text_response:
    token_count_chunk = token_utils.count_tokens(str(chunk))
    token_count += token_count_chunk
    page_text += str(chunk)    
    
pprint.pprint("Total token count = " + str(token_count))

# ADO Wiki pages does not have native 'Title' or 'Heading' attributes, have to generate these 
# Heading, Parse the Wiki Path on backslash, and take the last section of text
# Title is the Wiki Path with forwardslashes stripped
for char in '/':
    title = page.page.path.replace(char, ' ')
    heading = page.page.path.rsplit(char,1)[1]



page_one_dictionary = {"ADOUrl":page.page.url, "WikiPagePath":page.page.path, "Title":title, "Heading":heading, "Content":page_text, "Tokens":token_count}
#page_two_dictionary = {"ADOUrl":page.page.url, "WikiPagePath":page.page.path, "Content":page_text, "Tokens":token_count}
page_dictionary_list = [page_one_dictionary]
df = pd.DataFrame(page_dictionary_list)
pprint.pprint("Wiki Page Path = " + df["WikiPagePath"][0])

pprint.pprint("-=-=-=-=-= Begin generating questions -=-=-=-=-=")
df['context'] = df["Title"] + "\n" + df["Heading"] + "\n\n" + df["Content"]

# This statement will use Public OpenAI
#df['Questions'] = df["Content"].apply(generate_questions.generate_questions)

# This will use our Azure OpenAI isntance
df['Questions'] = df["Content"].apply(rest_azure_openai.create_questions)
df['Questions'] = "1." + df.Questions
print(df["Questions"].values[0:10])


pprint.pprint("-=-=-=-=-= Begin generating answers -=-=-=-=-=")
# This will use Public OpenAI
#df['Answers'] = df.apply(generate_answers.get_answers, axis=1)

# This will use our Auzre OpenAI isntance
df['Answers'] = df.apply(rest_azure_openai.create_answers, axis=1)
df['Answers'] = "1." + df.Answers
df = df.dropna().reset_index().drop('index',axis=1)
print(df[['Answers']].values[0][0])

pprint.pprint("-=-=-=-=-= Current Rows in the data set -=-=-=-=-=")
df = df.reset_index().set_index(["Title", "Heading"], drop=False)
print(f"{len(df)} rows in the data.")
print(df.sample(1))

# code below here is now fully functional, needs work
#commenting this out for now
#pprint.pprint("-=-=-=-=-= Begin generating embeddings -=-=-=-=-=")
# compute_doc_embeddings is currently set to call against OpenAi public instance
#document_embeddings = generate_embeddings.compute_doc_embeddings(df)

#example_entry = list(document_embeddings.items())[0]
#print(f"{example_entry[0]} : {example_entry[1][:5]}... ({len(example_entry[1])} entries)")

# To-Do - I do not think these are needed. Will delete once confirmed
#df['embeddings'] = df.apply(generate_embeddings.compute_doc_embeddings, axis=1)
#print(df[['embeddings']].values[0][0])

#pprint.pprint("-=-=-=-=-= Embeddings Created -=-=-=-=-=")
#pprint.pprint("-=-=-=-=-=-=-=-=-=-=")
#pprint.pprint("-=-=-=-=-= Answer the question without Prompt Engineering -=-=-=-=-=")
#no_prompt_engineering_answer = rest_azure_openai.base_completion(args.question)
#print(no_prompt_engineering_answer)

#pprint.pprint("-=-=-=-=-= Answer the question with Prompt Engineering -=-=-=-=-=")
#prompt = generate_embeddings.construct_prompt(
    #args.question,
    #document_embeddings,
    #df
#)

#pprint.pprint("-=-=-=-=-=-=-=-=-=-=")
#pprint.pprint("-=-=-=-=-= Engineered prompt created -=-=-=-=-=")
#print("===\n", prompt)
#prompt_engineering_answer = rest_azure_openai.base_completion(args.question)
#pprint.pprint("-=-=-=-=-=-=-=-=-=-=")
#pprint.pprint("-=-=-=-=-= Engineered prompt created -=-=-=-=-=")
#print(prompt_engineering_answer)

