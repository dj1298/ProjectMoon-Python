import os
import requests
import json

# Open AI REST API calls
# https://learn.microsoft.com/en-us/azure/cognitive-services/openai/reference
# 
# 
# Details on using 'requests' module
# https://www.nylas.com/blog/use-python-requests-module-rest-apis/#:~:text=The%20clear%2C%20simple%20syntax%20of%20Python%20makes%20it,HTTP%20requests%20to%20any%20API%20in%20the%20world.

azure_openai_endpoint = os.getenv('azure_openai_endpoint')
azure_openai_api_key = os.getenv('azure_openai_api_key')
azure_openai_deployment = os.getenv('azure_openai_deployment_id')
azure_openai_version = os.getenv('azure_openai_api_version')

 
# Create a completion
# POST https://{your-resource-name}.openai.azure.com/openai/deployments/{deployment-id}/completions?api-version={api-version}
# 
# Parameters
# prompt
# max_tokens
# temperature
# top_p
# n
# stream
# logprobs
# echo
# stop
# presences_penalty
# frequency_penalty
# best_of
# logit_bias
def create_completion(context):
    try:
        headers = {
            "api-key":azure_openai_api_key,
            "Content-Type":"application/json"
            }
        payload = {
            'model':'Davinci',
            'prompt':'Write questions based on the text below\n\nText: {context}\n\nQuestions:\n1.',
            'temperature':0.5,
            'max_tokens':1024,
            'top_p':1,
            'frequency_penalty':0,
            'presence_penalty':0,
            'stop':['\n\n']
            }

        response = requests.post(azure_openai_endpoint + 'openai/deployments/' + azure_openai_deployment + 
        '/completions?api-version=' + azure_openai_version,
        headers=headers, 
        data=json.dumps(payload))
        return(response)
    except requests.exceptions.HTTPError as errh:
        return(errh)
    except requests.exceptions.ConnectionError as errc:
        return(errc)
    except requests.exceptions.Timeout as errt:
        return(errt)
    except requests.exceptions.RequestException as err:
        return(err)




# Create an embedding
# POST https://{your-resource-name}.openai.azure.com/openai/deployments/{deployment-id}/embeddings?api-version={api-version}
#
# Parameters
# input
# user
# To-Do - Need to complete REST call code
def create_embedding(parameters):
    try:
        response = requests.post(azure_openai_endpoint + 'openai/deployments/' + azure_openai_deployment + 
        '/completions?api-version=' + azure_openai_version, 
        data = {
            "input":"",
            "user":""
        })
        return(response)
    except requests.exceptions.HTTPError as errh:
        return(errh)
    except requests.exceptions.ConnectionError as errc:
        return(errc)
    except requests.exceptions.Timeout as errt:
        return(errt)
    except requests.exceptions.RequestException as err:
        return(err)

