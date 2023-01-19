# ProjectMoon-Python
Python script that uses Azure Dev Ops module to get Wiki Data to train OpenAI instance.

Clone repo
From a command line 'pip install'
This will isntall all packages from teh requirements.txt file


set the following values lines in GetWikiPage.py
personal_access_token is your ADO token. Ensure it has read access for Wiki.
organization_url is the ADO Org URL.
wiki_page_path is the 'path' to a specific page, all teh way to the page name. ex. "Microsoft Teams/Teams Media/Media Connectivity/Port Usage"
openai.api_key is your own key from openai.com site

personal_access_token = ''
organization_url = 'https://dev.azure.com/Supportability'
wiki_page_path = "Microsoft Teams/Teams Media/Media Connectivity/Port Usage"
openai.api_key = ''


From a command line simply run .\GetWikiPage.py
The script will get the specified page and page content
Submit to openAi to generate questions
Submit questiosn to OpenAi to generate answers

As of 1-19-2023, the script needs to be developed so that it can create
embeddings. We should follow https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb
generate_embeddings.py is created, but currently not functional. 
More learning is required to understand and make this code work in this project. 
