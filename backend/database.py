"""
Database connection and utilities for DynamoDB.
"""
import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))


def get_dynamodb_resource():
    """Get DynamoDB resource configured with AWS credentials."""
    return boto3.resource(
        "dynamodb",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("MY_AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("MY_AWS_SECRET_ACCESS_KEY")
    )
