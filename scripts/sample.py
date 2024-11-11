import requests 
import os
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

cred = credentials.ApplicationDefault()

firebase_admin.initialize_app(cred)
db = firestore.client()
collection_name = "kubeflow_pipelines_instances"

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
  return response

create_client()

def get_client_values():
  url_1 = "https://dev.auth.mlops.ingka.com/admin/realms/istio/clients"
  payload = {}
  headers = {
  'Authorization': f'Bearer {access_token}'
  }
  response = requests.request("GET", url, headers=headers, data=payload)
  for data in response.json():
    if data['clientId']== f"client-{initiative_id}":
      client_uuid = data['id']

  url_2 = f"https://dev.auth.mlops.ingka.com/admin/realms/istio/clients/{client_uuid}/client-secret"
  response = requests.request("GET", url, headers=headers, data=payload)
  return response.json()['value']

client_sceret = get_client_values()

def update_firestore():
  docs = db.collection(collection_name).where(filter=FieldFilter("initiative_id", "==", initiative_id)).get()
  doc_id = docs[0].id
  metadata=db.collection(collection_name).document(doc_id)
  metadata.update({"cilent_id":f"client-{initiative_id}"})
  metadata.update({"client_sceret": client_sceret})

update_firestore()
  
