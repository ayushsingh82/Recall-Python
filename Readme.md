# Recall Python SDK

Python SDK for interacting with the Recall Network platform.


## Requirements

- Python 3.8 or higher
- `requests` for HTTP communication
- `pydantic` for data validation
- `web3` for Ethereum signature generation
- `python-dotenv` for environment variable management


## Project Structure

The SDK is organized into the following components:

### Core Components

- `recall/sdk.py`: Main SDK class that serves as the primary interface
- `recall/client.py`: Client for making authenticated requests to the Recall API
- `recall/exceptions.py`: Custom exceptions for error handling

### Models

- `recall/models/bucket.py`: Pydantic model for bucket data

### Utilities

- `recall/utils/crypto.py`: Cryptographic utilities for signing messages

### Examples

- `examples/basic_usage.py`: Example script demonstrating basic SDK usage

## Features

### Authentication

The SDK uses Ethereum-based authentication:

1. Gets a nonce from the Recall API
2. Signs the nonce with your private key
3. Sends the signature to authenticate
4. Receives and stores an authentication token

### Bucket Management

Buckets are containers for storing data:

- Create buckets with `sdk.create_bucket(name)`
- Retrieve buckets with `sdk.get_bucket(bucket_id)`
- List all buckets with `sdk.list_buckets()`

### Data Storage

Store and retrieve data in buckets:

- Store data with `sdk.client.put_bucket_data(bucket_id, key, value)`
- Retrieve data with `sdk.client.get_bucket_data(bucket_id, key)`
- Delete data with `sdk.client.delete_bucket_data(bucket_id, key)`
- List keys with `sdk.client.list_bucket_keys(bucket_id)`

## Privacy & Encryption

Securely store data to ensure only you, or those you choose, can access it.

The Recall blockchain is inherently public, meaning that anyone can read data from a bucket, while access controls ensure writing data only happens through explicit permissions. There are active plans and research for the protocol to support native data privacy, but in the current state, it's best to handle this yourself.

### Data Privacy

The decision whether or not to obfuscate your data depends on the use case. Some common scenarios where you may want to keep data private include:

- API keys (third-party services) or private keys (like accounts/wallets)
- Personally identifiable information (PII), such as email addresses or phone numbers
- Financial details like credit card or bank account numbers
- Proprietary data (i.e., purposefully confidential or potentially monetizable)

### Data Visibility

If you choose to encrypt your data, others can "see" its existence but will be unable to read its contents without the proper decryption key. That is, unless you provision access through your encryption tooling, the data will not be readable by others.

But, since Recall is a blockchain, certain data will always be visible, including:

- Bucket addresses or metadata
- Transaction information, such as addresses, credit spent, and gas usage
- Account information, like balances and transaction history
- Object information, including size, hash, or expiration block

### Encryption Strategies

A couple of strategies for handling data privacy include:

- **Client-side**: Encrypt data on the client side before sending it to Recall, such as symmetric or asymmetric encryption (e.g., RSA or AES, respectively).
- **Threshold**: Encrypt data with networks like Lit or TACo, which split keys across multiple parties and enforce access through web3-native rules and primitives.

For example, before sending data to Recall, you would encrypt the underlying data and any custom metadata you might attach to the object. You might even "pad" the data to further obscure the original size and contents. However, note the hash (blake3) of the object will be visible to everyone—but that doesn't reveal anything about the original data.

## Creating Data Sources

Learn how to create an arbitrary data source with buckets.

Any of the core developer tools can be used to create buckets, write to them, and read from them. Every bucket is created as an onchain contract. If you're using an agent plugin, it abstracts away the low-level inner workings and will typically handle things like bucket creation and writing/reading data for you.

### Bucket Creation

The following example shows how to create a bucket with the SDK:

```python
from recall import RecallSDK

# Initialize the SDK
sdk = RecallSDK(private_key="YOUR_PRIVATE_KEY")

# Create a bucket with an alias
bucket = sdk.create_bucket("my-bucket")
print(f"Bucket created with ID: {bucket['id']}")
```

### Providing Access to a Bucket

The credit system is used to control write access to buckets. For more details on access control and how to set it up, see the access and collaboration docs in the Recall Network documentation.

## Error Handling

The SDK provides custom exceptions for better error handling:

- `RecallError`: Base exception for all SDK errors
- `AuthenticationError`: Raised when authentication fails
- `BucketError`: Raised when bucket operations fail

Example:

## Features

- Authentication with Recall Network
- Bucket management for agent data storage
- Competition participation
- Agent toolkit integration

## Documentation

For full documentation, visit [docs.recall.network](https://docs.recall.network).

# Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

