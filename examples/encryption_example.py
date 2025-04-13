# This example demonstrates how to use encryption with the Recall Python SDK
import os
import json
import base64
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from recall import RecallSDK

# Load environment variables from .env file
load_dotenv()

class EncryptedStorage:
    """
    A helper class for encrypting and decrypting data stored in Recall buckets.
    
    This class uses Fernet symmetric encryption (AES-128 in CBC mode with PKCS7 padding)
    to encrypt data before storing it in a Recall bucket.
    """
    
    def __init__(self, sdk, password, salt=None):
        """
        Initialize the encrypted storage.
        
        Args:
            sdk: RecallSDK instance
            password: Password for encryption/decryption
            salt: Optional salt for key derivation (will be generated if not provided)
        """
        self.sdk = sdk
        
        # Generate or use provided salt
        self.salt = salt or os.urandom(16)
        
        # Derive encryption key from password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.cipher = Fernet(key)
    
    def create_bucket(self, name):
        """Create a new bucket."""
        return self.sdk.create_bucket(name)
    
    def encrypt_data(self, data):
        """
        Encrypt data before storing.
        
        Args:
            data: Data to encrypt (will be serialized to JSON)
            
        Returns:
            Encrypted data as a string
        """
        # Convert data to JSON string
        json_data = json.dumps(data)
        
        # Encrypt the JSON string
        encrypted_data = self.cipher.encrypt(json_data.encode())
        
        # Return base64 encoded encrypted data
        return base64.b64encode(encrypted_data).decode()
    
    def decrypt_data(self, encrypted_data):
        """
        Decrypt data after retrieval.
        
        Args:
            encrypted_data: Encrypted data as a string
            
        Returns:
            Decrypted data (deserialized from JSON)
        """
        # Decode base64 encoded encrypted data
        encrypted_bytes = base64.b64decode(encrypted_data)
        
        # Decrypt the data
        decrypted_data = self.cipher.decrypt(encrypted_bytes).decode()
        
        # Parse JSON and return
        return json.loads(decrypted_data)
    
    def put_data(self, bucket_id, key, data):
        """
        Encrypt and store data in a bucket.
        
        Args:
            bucket_id: ID of the bucket
            key: Key to store the data under
            data: Data to encrypt and store
        """
        encrypted_data = self.encrypt_data(data)
        self.sdk.client.put_bucket_data(bucket_id, key, encrypted_data)
    
    def get_data(self, bucket_id, key):
        """
        Retrieve and decrypt data from a bucket.
        
        Args:
            bucket_id: ID of the bucket
            key: Key to retrieve
            
        Returns:
            Decrypted data
        """
        encrypted_data = self.sdk.client.get_bucket_data(bucket_id, key)
        return self.decrypt_data(encrypted_data)
    
    def export_salt(self):
        """
        Export the salt for later use.
        
        Returns:
            Base64 encoded salt
        """
        return base64.b64encode(self.salt).decode()
    
    @classmethod
    def from_exported_salt(cls, sdk, password, salt_base64):
        """
        Create an instance using a previously exported salt.
        
        Args:
            sdk: RecallSDK instance
            password: Password for encryption/decryption
            salt_base64: Base64 encoded salt
            
        Returns:
            EncryptedStorage instance
        """
        salt = base64.b64decode(salt_base64)
        return cls(sdk, password, salt)


def main():
    # Initialize the SDK with private key from environment
    sdk = RecallSDK()
    
    # Create encrypted storage with a password
    # In a real application, you would want to securely manage this password
    storage = EncryptedStorage(sdk, password="your-secure-password")
    
    # Create a new bucket
    bucket = storage.create_bucket("encrypted-bucket")
    print(f"Created bucket: {bucket['name']} (ID: {bucket['id']})")
    
    # Store sensitive data in the bucket (will be encrypted)
    sensitive_data = {
        "api_key": "sk_test_abcdefghijklmnopqrstuvwxyz123456",
        "user_info": {
            "email": "user@example.com",
            "phone": "555-123-4567",
            "address": "123 Main St, Anytown, USA"
        },
        "payment_details": {
            "card_number": "XXXX-XXXX-XXXX-1234",
            "expiry": "12/25",
            "cvv": "XXX"
        }
    }
    
    storage.put_data(bucket["id"], "sensitive-info", sensitive_data)
    print("Stored encrypted sensitive data in bucket")
    
    # Export the salt for future sessions
    # You need to store this securely to decrypt the data later
    salt_base64 = storage.export_salt()
    print(f"Salt (save this securely): {salt_base64}")
    
    # Simulate a new session by creating a new storage instance with the exported salt
    new_storage = EncryptedStorage.from_exported_salt(sdk, "your-secure-password", salt_base64)
    
    # Retrieve and decrypt the data
    retrieved_data = new_storage.get_data(bucket["id"], "sensitive-info")
    print("\nRetrieved and decrypted data:")
    print(json.dumps(retrieved_data, indent=2))
    
    # Verify the data matches
    assert retrieved_data == sensitive_data, "Decrypted data doesn't match original data!"
    print("\nSuccess! The decrypted data matches the original data.")


if __name__ == "__main__":
    main() 