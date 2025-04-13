import os
from typing import Dict, Any, Optional, List
import requests

from .client import RecallClient
from .exceptions import RecallError, AuthenticationError

class RecallSDK:
    """
    Main SDK class for interacting with Recall Network.
    """
    
    def __init__(
        self, 
        private_key: Optional[str] = None,
        api_url: str = "https://api.recall.network",
        chain_id: int = 1,
    ):
        """
        Initialize the Recall SDK.
        
        Args:
            private_key: Ethereum private key for authentication
            api_url: Base URL for the Recall API
            chain_id: Chain ID for the network
        """
        self.api_url = api_url
        self.chain_id = chain_id
        
        # Use provided private key or try to get from environment
        self._private_key = private_key or os.environ.get("RECALL_PRIVATE_KEY")
        if not self._private_key:
            raise AuthenticationError("Private key is required. Provide it directly or set RECALL_PRIVATE_KEY environment variable.")
        
        # Initialize client with authentication
        self.client = RecallClient(
            api_url=api_url,
            private_key=self._private_key,
            chain_id=chain_id
        )
    
    def create_bucket(self, name: str) -> Dict[str, Any]:
        """
        Create a new bucket for data storage.
        
        Args:
            name: Name of the bucket
            
        Returns:
            Bucket data
        """
        return self.client.create_bucket(name)
    
    def get_bucket(self, bucket_id: str) -> Dict[str, Any]:
        """
        Get an existing bucket by ID.
        
        Args:
            bucket_id: ID of the bucket to retrieve
            
        Returns:
            Bucket data
        """
        return self.client.get_bucket(bucket_id)
    
    def list_buckets(self) -> List[Dict[str, Any]]:
        """
        List all buckets owned by the authenticated user.
        
        Returns:
            List of bucket data
        """
        return self.client.list_buckets()
