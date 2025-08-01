import requests
import json
from datetime import datetime
import re
import os

def get_pokemon_groups():
  # url for all pokemon groups
  url = "https://tcgcsv.com/tcgplayer/3/groups"
  response = requests.get(url)

  if response.status_code != 200:
    print(f"Failed to fetch. Status code: {response.status_code}")
    return
  
  timestamp = datetime.now().isoformat()
  data = response.json()
  groups = [{"name": set["name"], "groupId": set["groupId"],
            "timestamp": timestamp} for set in data["results"]]
  groups = sorted(groups, key=lambda x: x["groupId"])

  with open("groups.json", "w", encoding="utf-8") as f:
    json.dump(groups, f, ensure_ascii=False, indent=2)

def get_pokemon_products(groupId, name):
  url = f"https://tcgcsv.com/tcgplayer/3/{groupId}/products"

  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    results = data["results"]

    if not results:
      print(f"Skipping products for {name} - {groupId}. No results.")
      return

    timestamp = datetime.now().isoformat()
    products = [{"productId": item["productId"], "name": item["name"], "imageUrl": item["imageUrl"], "timestamp": timestamp}
              for item in results]
    
    safe_name = re.sub(r'[^\w\-_. ]', '', name).replace(" ", "_")
    file_name = f"../data/raw/{safe_name}_{groupId}_products.json"
    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    with open(file_name, "w", encoding="utf-8") as f:
      json.dump(products, f, ensure_ascii=False, indent=2)

def get_pokemon_prices(groupId, name):
  url = f"https://tcgcsv.com/tcgplayer/3/{groupId}/prices"

  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    results = data["results"]

    if not results:
      print(f"Skipping prices {name} - {groupId}. No results")
      return
    
    timestamp = datetime.now().isoformat()
    products = [{"productId": item["productId"], "marketPrice": item["marketPrice"], "timestamp": timestamp}
                for item in results]
    
    safe_name = re.sub(r'[^\w\-_. ]', '', name).replace(" ", "_")
    file_name = f"../data/raw/{safe_name}_{groupId}_prices.json"
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    
    with open(file_name, "w", encoding="utf-8") as f:
      json.dump(products, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
  get_pokemon_groups()
  with open("groups.json", "r", encoding="utf-8") as f:
    groups = json.load(f)
  for group in groups:
      get_pokemon_products(group["groupId"], group["name"])
      get_pokemon_prices(group["groupId"], group["name"])

