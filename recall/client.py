# This file contains the RecallClient class that handles API communication
import os
from typing import Dict, Any, Optional, List
import requests
from web3 import Web3

from .exceptions import RecallError, AuthenticationError

class RecallClient:
    """
    Client for making authenticated requests to the Recall API.
    
    This class handles the low-level communication with the Recall Network API,
    including authentication, request signing, and error handling.
    """
    
    def __init__(
        self, 
        api_url: str,
        private_key: str,
        chain_id: int = 1,
    ):
        """
        Initialize the Recall API client.
        
        Sets up the Web3 account and authenticates with the API.
        
        Args:
            api_url: Base URL for the Recall API
            private_key: Ethereum private key for authentication
            chain_id: Chain ID for the network
        """
        self.api_url = api_url
        self._private_key = private_key
        self.chain_id = chain_id
        
        # Initialize Web3 for signing
        # This creates an Ethereum account from the private key
        self.web3 = Web3()
        self.account = self.web3.eth.account.from_key(self._private_key)
        self.address = self.account.address
        
        # Initialize session with authentication
        # Using a session allows for connection pooling and maintaining headers
        self.session = requests.Session()
        self._authenticate()
    
    def _authenticate(self) -> None:
        """
        Authenticate with the Recall API using the private key.
        
        This method:
        1. Gets a nonce from the server
        2. Signs the nonce with the private key
        3. Sends the signature to get an authentication token
        4. Sets the token in the session headers
        """
        try:
            # Get nonce from server
            # The nonce ensures each signature is unique
            nonce_response = self.session.get(f"{self.api_url}/auth/nonce?address={self.address}")
            nonce_response.raise_for_status()
            nonce_data = nonce_response.json()
            nonce = nonce_data["nonce"]
            
            # Sign the nonce
            # This proves ownership of the private key
            message = f"Sign this message to authenticate with Recall Network: {nonce}"
            signed_message = self.web3.eth.account.sign_message(
                text=message,
                private_key=self._private_key
            )
            
            # Authenticate with the signature
            # The server verifies the signature and issues a token
            auth_response = self.session.post(
                f"{self.api_url}/auth/login",
                json={
                    "address": self.address,
                    "signature": signed_message.signature.hex(),
                }
            )
            auth_response.raise_for_status()
            auth_data = auth_response.json()
            
            # Set the token in session headers
            # This token will be used for all subsequent requests
            self.session.headers.update({
                "Authorization": f"Bearer {auth_data['token']}"
            })
            
        except requests.RequestException as e:
            raise AuthenticationError(f"Failed to authenticate: {str(e)}")
    
    def create_bucket(self, name: str) -> Dict[str, Any]:
        """
        Create a new bucket for data storage.
        
        Makes a POST request to create a bucket with the given name.
        
        Args:
            name: Name of the bucket
            
        Returns:
            Bucket data from the API response
        """
        try:
            response = self.session.post(
                f"{self.api_url}/buckets",
                json={"name": name}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise RecallError(f"Failed to create bucket: {str(e)}")
    
    def get_bucket(self, bucket_id: str) -> Dict[str, Any]:
        """
        Get an existing bucket by ID.
        
        Makes a GET request to retrieve bucket information.
        
        Args:
            bucket_id: ID of the bucket to retrieve
            
        Returns:
            Bucket data from the API response
        """
        try:
            response = self.session.get(f"{self.api_url}/buckets/{bucket_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise RecallError(f"Failed to get bucket: {str(e)}")
    
    def list_buckets(self) -> List[Dict[str, Any]]:
        """
        List all buckets owned by the authenticated user.
        
        Makes a GET request to retrieve all buckets.
        
        Returns:
            List of bucket data objects from the API response
        """
        try:
            response = self.session.get(f"{self.api_url}/buckets")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise RecallError(f"Failed to list buckets: {str(e)}")
    
    def put_bucket_data(self, bucket_id: str, key: str, value: Any) -> None:
        """
        Store data in a bucket.
        
        Makes a PUT request to store data under a specific key.
        
        Args:
            bucket_id: ID of the bucket
            key: Key to store the data under
            value: Data to store (will be serialized to JSON)
        """
        try:
            response = self.session.put(
                f"{self.api_url}/buckets/{bucket_id}/data/{key}",
                json={"value": value}
            )
            response.raise_for_status()
        except requests.RequestException as e:
            raise RecallError(f"Failed to store data: {str(e)}")
    
    def get_bucket_data(self, bucket_id: str, key: str) -> Any:
        """
        Retrieve data from a bucket.
        
        Makes a GET request to retrieve data stored under a specific key.
        
        Args:
            bucket_id: ID of the bucket
            key: Key to retrieve
            
        Returns:
            The stored data (deserialized from JSON)
        """
        try:
            response = self.session.get(
                f"{self.api_url}/buckets/{bucket_id}/data/{key}"
            )
            response.raise_for_status()
            data = response.json()
            return data["value"]
        except requests.RequestException as e:
            raise RecallError(f"Failed to retrieve data: {str(e)}")
    
    def delete_bucket_data(self, bucket_id: str, key: str) -> None:
        """
        Delete data from a bucket.
        
        Makes a DELETE request to remove data stored under a specific key.
        
        Args:
            bucket_id: ID of the bucket
            key: Key to delete
        """
        try:
            response = self.session.delete(
                f"{self.api_url}/buckets/{bucket_id}/data/{key}"
            )
            response.raise_for_status()
        except requests.RequestException as e:
            raise RecallError(f"Failed to delete data: {str(e)}")
    
    def list_bucket_keys(self, bucket_id: str) -> List[str]:
        """
        List all keys in a bucket.
        
        Makes a GET request to retrieve all keys in a bucket.
        
        Args:
            bucket_id: ID of the bucket
            
        Returns:
            List of keys as strings
        """
        try:
            response = self.session.get(
                f"{self.api_url}/buckets/{bucket_id}/data"
            )
            response.raise_for_status()
            data = response.json()
            return data["keys"]
        except requests.RequestException as e:
            raise RecallError(f"Failed to list keys: {str(e)}")
