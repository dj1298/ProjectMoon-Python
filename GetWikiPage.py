from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v6_0.wiki import WikiClient
import pprint
import numpy as np
import pandas as pd
import openai

import generate_questions
import generate_answers
import generate_embeddings
import token_utils


# ADO Personal access token, ADO URL, OpenAI Key
personal_access_token = ''
organization_url = 'https://dev.azure.com/Supportability'
wiki_page_path = "Microsoft Teams/Teams Media/Media Connectivity/Port Usage"
openai.api_key = ''


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
page_text_response = wiki_client.get_page_text(project="UC", wiki_identifier="UC.wiki", path="Microsoft Teams/Teams Media/Media Connectivity/Port Usage", include_content=True)
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

page_one_dictionary = {"ADOUrl":page.page.url, "WikiPagePath":page.page.path, "Content":page_text, "Tokens":token_count}
#page_two_dictionary = {"ADOUrl":page.page.url, "WikiPagePath":page.page.path, "Content":page_text, "Tokens":token_count}
page_dictionary_list = [page_one_dictionary]
df = pd.DataFrame(page_dictionary_list)
pprint.pprint("Wiki Page Path = " + df["WikiPagePath"][0])

pprint.pprint("-=-=-=-=-= Begin generating questions -=-=-=-=-=")
df['context'] = df["ADOUrl"] + "\n" + df["WikiPagePath"] + "\n\n" + df["Content"]
df['Questions'] = df["Content"].apply(generate_questions.generate_questions)
df['Questions'] = "1." + df.Questions
print(df["Questions"].values[0:10])


pprint.pprint("-=-=-=-=-= Begin generating answers -=-=-=-=-=")
df['Answers'] = df.apply(generate_answers.get_answers, axis=1)
df['Answers'] = "1." + df.Answers
df = df.dropna().reset_index().drop('index',axis=1)
print(df[['Answers']].values[0][0])

pprint.pprint("-=-=-=-=-= Begin generating embeddings -=-=-=-=-=")

document_embeddings = generate_embeddings.compute_doc_embeddings(df)
print(document_embeddings)
#df['embeddings'] = df.apply(generate_embeddings.compute_doc_embeddings, axis=1)
#print(df[['embeddings']].values[0][0])
