"""
Initialize the User DynamoDB table.
"""
import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

TABLE_NAME = "User"
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


def get_dynamodb_client():
    """Get DynamoDB client configured with AWS credentials."""
    return boto3.client(
        "dynamodb",
        region_name=AWS_REGION,
        aws_access_key_id=os.getenv("MY_AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("MY_AWS_SECRET_ACCESS_KEY")
    )


def create_user_table_if_not_exists():
    """Create the User table if it doesn't exist."""
    dynamodb_client = get_dynamodb_client()
    
    try:
        # Check if table exists
        dynamodb_client.describe_table(TableName=TABLE_NAME)
        print(f"Table '{TABLE_NAME}' already exists.")
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            # Table doesn't exist, create it
            try:
                print(f"Creating table '{TABLE_NAME}'...")
                table_schema = {
                    "TableName": TABLE_NAME,
                    "KeySchema": [
                        {"AttributeName": "username", "KeyType": "HASH"}
                    ],
                    "AttributeDefinitions": [
                        {"AttributeName": "username", "AttributeType": "S"}
                    ],
                    "BillingMode": "PAY_PER_REQUEST"
                }
                dynamodb_client.create_table(**table_schema)
                
                # Wait for table to be created
                waiter = dynamodb_client.get_waiter("table_exists")
                waiter.wait(TableName=TABLE_NAME)
                print(f"Table '{TABLE_NAME}' created successfully.")
                return True
            except ClientError as create_error:
                print(f"Error creating table: {create_error}")
                return False
        else:
            print(f"Error checking table: {e}")
            return False


def main():
    """Main function to initialize User table."""
    print("Initializing User DynamoDB table...")
    
    if create_user_table_if_not_exists():
        print("\nUser table initialization completed successfully!")
    else:
        print("\nUser table initialization failed!")


if __name__ == "__main__":
    main()

