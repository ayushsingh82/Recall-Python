class RecallError(Exception):
    """Base exception for all Recall SDK errors."""
    pass

class AuthenticationError(RecallError):
    """Raised when authentication fails."""
    pass

class BucketError(RecallError):
    """Raised when bucket operations fail."""
    pass
