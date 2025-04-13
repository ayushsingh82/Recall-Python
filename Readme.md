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

