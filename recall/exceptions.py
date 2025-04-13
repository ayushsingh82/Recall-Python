# This file defines custom exceptions for the SDK
# Using custom exceptions allows for more specific error handling

class RecallError(Exception):
    """
    Base exception for all Recall SDK errors.
    
    All other exceptions in the SDK inherit from this class,
    allowing users to catch all SDK-related errors with a single except block.
    """
    pass

class AuthenticationError(RecallError):
    """
    Raised when authentication fails.
    
    This could be due to:
    - Missing private key
    - Invalid private key
    - Server authentication issues
    """
    pass

class BucketError(RecallError):
    """
    Raised when bucket operations fail.
    
    This could be due to:
    - Bucket not found
    - Permission issues
    - Invalid data format
    """
    pass
