import requests
import json
from datetime import datetime
import re

timestamp = datetime.now().isoformat()

def get_pokemon_groups():
  # url for all pokemon groups
  url = "https://tcgcsv.com/tcgplayer/3/groups"
  response = requests.get(url)

  if response.status_code != 200:
    print(f"Failed to fetch. Status code: {response.status_code}")
    return
  
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
    products = [{"productId": item["productId"], "name": item["name"], "imageUrl": item["imageUrl"], "timestamp": timestamp}
              for item in results]
    with open(f"../data/raw/{name}_{groupId}_products.json", "w", encoding="utf-8") as f:
      json.dump(products, f, ensure_ascii=False, indent=2)

def get_pokemon_prices(groupId, name):
  url = f"https://tcgcsv.com/tcgplayer/3/{groupId}/prices"

  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    results = data["results"]
    products = [{"productId": item["productId"], "marketPrice": item["marketPrice"], "timestamp": timestamp}
                for item in results]
    with open(f"../data/raw/{name}_{groupId}_prices.json", "w", encoding="utf-8") as f:
      json.dump(products, f, ensure_ascii=False, indent=2)


with open("groups.json", "r", encoding="utf-8") as f:
    groups = json.load(f)

if __name__ == "__main__":
  # get_pokemon_groups()
  for group in groups:
      print(group)
      group_id = group["groupId"]
      name = re.sub(r'[^\w\-_. ]', '', group["name"]).replace(" ", "_")
      get_pokemon_products(group_id, name)
      get_pokemon_prices(group_id, name)

