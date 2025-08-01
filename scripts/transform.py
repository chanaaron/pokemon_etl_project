import json
import os
import pandas as pd
from datetime import datetime
def load_json_to_df(path):
    with open(path, "r", encoding="utf-8") as f:
        return pd.DataFrame(json.load(f))


def transform_all_groups():
    raw_dir = "../data/raw"
    output_dir = "../data/processed"
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(raw_dir):
        if filename.endswith("_products.json"):
            base_name = filename.replace("_products.json", "")
            products_path = os.path.join(raw_dir, f"{base_name}_products.json")
            prices_path = os.path.join(raw_dir, f"{base_name}_prices.json")

            if not os.path.exists(prices_path):
                print(f"Skipping group {base_name} — no price file.")
                continue

            with open(products_path, encoding="utf-8") as f:
                products_data = json.load(f)

            with open(prices_path, encoding="utf-8") as f:
                prices_data = json.load(f)

            if not products_data or not prices_data:
                print(
                    f"Skipping group {base_name} — one of the files is empty.")
                continue

            df_products = pd.DataFrame(products_data)
            df_prices = pd.DataFrame(prices_data)

            if "productId" not in df_products.columns or "productId" not in df_prices.columns:
                print(
                    f"Skipping group {base_name} — missing 'productId' in one of the files.")
                continue

            df = pd.merge(df_products, df_prices, on="productId", how="inner")

            df["extracted_timestamp"] = df[["timestamp_x", "timestamp_y"]].max(axis=1)
            df = df.drop(columns=["timestamp_x", "timestamp_y"])
            df["transformed_at"] = datetime.now().isoformat()

            df.to_csv(os.path.join(
                output_dir, f"{base_name}_combined.csv"), index=False)
            print(f"Saved: {base_name}_combined.csv")


if __name__ == "__main__":
  transform_all_groups()
