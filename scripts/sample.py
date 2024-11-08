import requests 
import os

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_access_token():
  print("Getting access token", client_id, client_secret)
  return client_id, client_secret
