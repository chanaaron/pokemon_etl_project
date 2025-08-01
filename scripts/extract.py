import requests
import json

def get_pokemon_groups():
  # url for all pokemon groups
  url = "https://tcgcsv.com/tcgplayer/3/groups"

  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    results = data["results"]
    groups = [{"name": set["name"], "groupId": set["groupId"]} for set in results]
    groups = sorted(groups, key=lambda x: x["groupId"])
    with open("groups.json", "w", encoding="utf-8") as f:
      json.dump(groups, f, ensure_ascii=False, indent=2)

def get_pokemon_products(groupId):
  url = f"https://tcgcsv.com/tcgplayer/3/{groupId}/products"

  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    results = data["results"]
    products = [{"productId": item["productId"], "name": item["name"], "imageUrl": item["imageUrl"]}
              for item in results]
    with open(f"../data/raw/{groupId}_products.json", "w", encoding="utf-8") as f:
      json.dump(products, f, ensure_ascii=False, indent=2)

def get_pokemon_prices(groupId):
  url = f"https://tcgcsv.com/tcgplayer/3/{groupId}/prices"

  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    results = data["results"]
    for t in results:
      print(t['productId'], t['marketPrice'])

    products = [{"productId": item["productId"], "marketPrice": item["marketPrice"]}
                for item in results]
    with open(f"../data/raw/{groupId}_prices.json", "w", encoding="utf-8") as f:
      json.dump(products, f, ensure_ascii=False, indent=2)


with open("groups.json", "r", encoding="utf-8") as f:
    groups = json.load(f)

if __name__ == "__main__":
  for group in groups:
      group_id = group["groupId"]
      get_pokemon_products(group_id)
      get_pokemon_prices(group_id)

