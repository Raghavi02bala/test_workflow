import requests 
import os

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def create_access_token():
  url = "https://dev.auth.mlops.ingka.com/realms/istio/protocol/openid-connect/token"
  payload = f'client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials'
  headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
  }
  
  response = requests.request("POST", url, headers=headers, data=payload)
  return response

print(create_access_token())

