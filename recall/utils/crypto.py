from typing import Dict, Any
from web3 import Web3

def sign_message(private_key: str, message: str) -> Dict[str, Any]:
    """
    Sign a message with a private key.
    
    Args:
        private_key: Ethereum private key
        message: Message to sign
        
    Returns:
        Dictionary with signature details
    """
    web3 = Web3()
    signed_message = web3.eth.account.sign_message(
        text=message,
        private_key=private_key
    )
    
    return {
        "message": message,
        "messageHash": signed_message.messageHash.hex(),
        "signature": signed_message.signature.hex(),
        "r": signed_message.r,
        "s": signed_message.s,
        "v": signed_message.v
    } 