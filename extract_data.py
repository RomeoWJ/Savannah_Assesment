import requests, json
from google.cloud import storage

def extract_and_upload(api_url, filename, bucket_name):
    response = requests.get(api_url)
    data = response.json()

    # Save locally
    with open(filename, 'w') as f:
        json.dump(data, f)

    # Upload to GCS
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)
    print(f"Uploaded {filename} to GCS bucket {bucket_name}")

def run_extraction():
    bucket_name = "savannah-data-pipeline-bucket"
    apis = {
        "users.json": "https://dummyjson.com/users",
        "products.json": "https://dummyjson.com/products",
        "carts.json": "https://dummyjson.com/carts"
    }

    for filename, url in apis.items():
        extract_and_upload(url, filename, bucket_name)

if __name__ == "__main__":
    run_extraction()
