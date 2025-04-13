import os
from dotenv import load_dotenv
from recall import RecallSDK

# Load environment variables from .env file
load_dotenv()

def main():
    # Initialize the SDK with private key from environment
    sdk = RecallSDK()
    
    # Create a new bucket
    bucket = sdk.create_bucket("example-bucket")
    print(f"Created bucket: {bucket['name']} (ID: {bucket['id']})")
    
    # Store data in the bucket
    data = {
        "name": "Example Agent",
        "capabilities": ["text-generation", "image-recognition"],
        "settings": {
            "temperature": 0.7,
            "max_tokens": 1000
        }
    }
    sdk.client.put_bucket_data(bucket["id"], "agent-config", data)
    print("Stored agent configuration in bucket")
    
    # Retrieve data from the bucket
    retrieved_data = sdk.client.get_bucket_data(bucket["id"], "agent-config")
    print("Retrieved data:", retrieved_data)
    
    # List all buckets
    buckets = sdk.list_buckets()
    print(f"Found {len(buckets)} buckets:")
    for b in buckets:
        print(f"- {b['name']} (ID: {b['id']})")

if __name__ == "__main__":
    main() 