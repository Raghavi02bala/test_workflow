import requests 
import os

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
initiative_id = os.getenv("INITIATIVE_ID")
team_name = os.getenv("TEAM_NAME")
env = os.getenv("ENVIRONMENT")

def create_access_token():
  url = "https://dev.auth.mlops.ingka.com/realms/istio/protocol/openid-connect/token"
  payload = f'client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials'
  headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
  }
  
  response = requests.request("POST", url, headers=headers, data=payload)
  return response.json()['access_token']

access_token = create_access_token()

def create_client():
  url = "https://dev.auth.mlops.ingka.com/admin/realms/istio/clients"
  payload = json.dumps({
    "clientId": f"client-{initiative_id}",
    "rootUrl": f"http://{initiative_id}.{team_name}.{env}.mlops.ingka.com",
    "redirectUris": [
      f"http://{initiative_id}.{team_name}.{env}.mlops.ingka.com"
    ]
  })
  headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {access_token}'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  return response.json()
