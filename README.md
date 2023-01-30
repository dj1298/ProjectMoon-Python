# ProjectMoon-Python
Python script that uses Azure Dev Ops module to get Wiki Data to train OpenAI instance.


You will need to install the Rust installer first https://www.rust-lang.org/tools/install
If this is not installed, then the 'Transformers' package will fail to build


Clone repo
Open folder in VS Code


First, create a virtual environment for the script
Open a terminal window and run 
    py -m venv venv


Then go to View\Command pallete
Type in 'Python: Select interpreter'
Select the 'venv' environment
    If you miss this step, all requirements will install to the Python global environment, not venv.



From a command line 'pip install --requirement requirements.txt'
   *I did have an issue where packages would not install with access deny. 
   if you hit this problem, open VS Code as Admin, or you can open a open a CMD prompt as Admin and install from there.
   
   
This will isntall all packages from the requirements.txt file

Look in code explorer, under venv\LIB\site-packages

You should see all of the packages

If they are not there, then will have to go down the path of uninstalling each package individually from global.

Then install correctly into the venv. 

There is also an option to set Pythin to look in global, but not sure this is best idea. 


Set the following values lines in .env file

The git ignore file will prevent this .env file from being tracked in source control. 
    
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
