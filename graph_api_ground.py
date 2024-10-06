import requests
import os

from dotenv import load_dotenv

load_dotenv()

tenant_id = os.getenv('tenant_id')
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret_value')

token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
graph_user_url = 'https://graph.microsoft.com/v1.0/users'

# function to get access token
def get_access_token():
    request_payload = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': 'https://graph.microsoft.com/.default'
    }
    response = requests.post(token_url, data=request_payload)
    token_response = response.json()
    access_token = token_response.get('access_token')
    return access_token

def get_all_users(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(graph_user_url, headers=headers)

    if response.status_code == 200:
        users = response.json()
        print("user details :")
        print(users)
    else:
        print("error retrieving data", response.status_code, response.text)

def filter_users(access_token, search_element):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    request_payload = {
        "$filter": f"startswith(displayName, '{search_element}') or startswith(mail, '{search_element}')",
    }
    response = requests.get(graph_user_url, headers=headers, params=request_payload) 

    if response.status_code == 200:
        users = response.json()
        print("Result from filtering user")
        print("user details :")
        print(users)
    else:
        print("error retrieving data", response.status_code, response.text)
            

if __name__ == "__main__":
    access_token = get_access_token()
    get_all_users(access_token)
    search_element = "mesampathhere@gmail.com"
    filter_users(access_token, search_element)
