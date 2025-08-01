import json
import os
import pandas as pd

def load_json_to_df(path):
    with open(path, "r", encoding="utf-8") as f:
        return pd.DataFrame(json.load(f))


def transform_all_groups():
    raw_dir = "../data/raw"
    output_dir = "../data/processed"
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(raw_dir):
        if filename.endswith("_products.json"):
            group_id = filename.split("_")[0]
            products_path = os.path.join(raw_dir, f"{group_id}_products.json")
            prices_path = os.path.join(raw_dir, f"{group_id}_prices.json")

            if not os.path.exists(prices_path):
                print(f"Skipping group {group_id} — no price file.")
                continue

            with open(products_path, encoding="utf-8") as f:
                products_data = json.load(f)

            with open(prices_path, encoding="utf-8") as f:
                prices_data = json.load(f)

            if not products_data or not prices_data:
                print(
                    f"Skipping group {group_id} — one of the files is empty.")
                continue

            df_products = pd.DataFrame(products_data)
            df_prices = pd.DataFrame(prices_data)

            if "productId" not in df_products.columns or "productId" not in df_prices.columns:
                print(
                    f"Skipping group {group_id} — missing 'productId' in one of the files.")
                continue

            df = pd.merge(df_products, df_prices, on="productId", how="inner")
            df.to_csv(os.path.join(
                output_dir, f"{group_id}_combined.csv"), index=False)
            print(f"Saved: {group_id}_combined.csv")
# def transform_all_groups():
#   groups = json.load(open("./groups.json", encoding="utf-8"))
#   all_rows = []

#   for group in groups:
#     group_id = group["groupId"]
#     group_name = group["name"]

#     products_path = f"../data/raw/{group_id}_products.json"
#     prices_path = f"../data/raw/{group_id}_prices.json"

#     if not os.path.exists(products_path) or not os.path.exists(prices_path):
#         continue

#     df_products = load_json_to_df(products_path)
#     df_prices = load_json_to_df(prices_path)

#     df = pd.merge(df_products, df_prices, on="productId", how="inner")
#     df["groupId"] = group_id
#     df["groupName"] = group_name

#     all_rows.append(df)

#   final_df = pd.concat(all_rows, ignore_index=True)
#   os.makedirs("../data/clean", exist_ok=True)
#   final_df.to_csv("../data/clean/pokemon_prices.csv", index=False)


if __name__ == "__main__":
  transform_all_groups()
