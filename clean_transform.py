import pandas as pd
import json


# --- USERS CLEANING ---
def clean_users(file_path):
    with open(file_path) as f:
        data = json.load(f)

    df = pd.json_normalize(data['users'])

    # Calculate age from birthDate
    df['age'] = 2025 - pd.to_datetime(df['birthDate']).dt.year

    # Rename and select useful columns
    df = df.rename(columns={
        'id': 'user_id',
        'firstName': 'first_name',
        'lastName': 'last_name',
        'address.address': 'street',
        'address.city': 'city',
        'address.postalCode': 'postal_code'
    })

    df = df[['user_id', 'first_name', 'last_name', 'gender', 'age', 'street', 'city', 'postal_code']]
    return df


# --- PRODUCTS CLEANING ---
def clean_products(file_path):
    with open(file_path) as f:
        data = json.load(f)

    df = pd.json_normalize(data['products'])

    # Exclude products with price <= 50
    df = df[df['price'] > 50]

    # Rename columns
    df = df.rename(columns={
        'id': 'product_id',
        'title': 'name'
    })

    df = df[['product_id', 'name', 'category', 'brand', 'price']]
    return df


# --- CARTS CLEANING ---
def clean_carts(file_path):
    with open(file_path) as f:
        data = json.load(f)

    df = pd.json_normalize(
        data['carts'],
        record_path=['products'],
        meta=['id', 'userId', 'total'],
        record_prefix='product_'
    )

    df = df.rename(columns={
        'id': 'cart_id',
        'userId': 'user_id',
        'product_id': 'product_id',
        'product_quantity': 'quantity',
        'product_price': 'price',
        'total': 'total_cart_value'
    })

    keep_cols = ['cart_id', 'user_id', 'product_id', 'quantity', 'price', 'total_cart_value']
    df = df[[col for col in keep_cols if col in df.columns]]

    return df


# --- PIPELINE WRAPPER ---
def run_cleaning():
    """Cleans and saves users, products, and carts data locally."""
    print("🧹 Cleaning datasets...")

    users = clean_users("users.json")
    products = clean_products("products.json")
    carts = clean_carts("carts.json")

    users.to_csv("clean_users.csv", index=False)
    products.to_csv("clean_products.csv", index=False)
    carts.to_csv("clean_carts.csv", index=False)

    print("Cleaned data saved locally.")


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    run_cleaning()
