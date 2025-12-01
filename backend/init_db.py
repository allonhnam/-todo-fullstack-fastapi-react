"""
Initialize DynamoDB table and seed test data.
"""
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from uuid import uuid4
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Table configuration
TODO_TABLE_NAME = "Todo"
USER_TABLE_NAME = "User"
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


def get_dynamodb_client():
    """Get DynamoDB client configured with AWS credentials."""
    return boto3.client(
        "dynamodb",
        region_name=AWS_REGION,
        aws_access_key_id=os.getenv("MY_AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("MY_AWS_SECRET_ACCESS_KEY")
    )


def get_dynamodb_resource():
    """Get DynamoDB resource configured with AWS credentials."""
    return boto3.resource(
        "dynamodb",
        region_name=AWS_REGION,
        aws_access_key_id=os.getenv("MY_AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("MY_AWS_SECRET_ACCESS_KEY")
    )


def create_table_if_not_exists(table_name, key_schema, attribute_definitions):
    """Create a DynamoDB table if it doesn't exist."""
    dynamodb_client = get_dynamodb_client()
    
    try:
        # Check if table exists
        dynamodb_client.describe_table(TableName=table_name)
        print(f"Table '{table_name}' already exists.")
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            # Table doesn't exist, create it
            try:
                print(f"Creating table '{table_name}'...")
                table_schema = {
                    "TableName": table_name,
                    "KeySchema": key_schema,
                    "AttributeDefinitions": attribute_definitions,
                    "BillingMode": "PAY_PER_REQUEST"
                }
                dynamodb_client.create_table(**table_schema)
                
                # Wait for table to be created
                waiter = dynamodb_client.get_waiter("table_exists")
                waiter.wait(TableName=table_name)
                print(f"Table '{table_name}' created successfully.")
                return True
            except ClientError as create_error:
                print(f"Error creating table: {create_error}")
                return False
        else:
            print(f"Error checking table: {e}")
            return False


def create_todo_table():
    """Create the Todo table if it doesn't exist."""
    return create_table_if_not_exists(
        table_name=TODO_TABLE_NAME,
        key_schema=[
            {"AttributeName": "user_id", "KeyType": "HASH"},
            {"AttributeName": "todo_id", "KeyType": "RANGE"}
        ],
        attribute_definitions=[
            {"AttributeName": "user_id", "AttributeType": "S"},
            {"AttributeName": "todo_id", "AttributeType": "S"}
        ]
    )


def create_user_table():
    """Create the User table if it doesn't exist."""
    return create_table_if_not_exists(
        table_name=USER_TABLE_NAME,
        key_schema=[
            {"AttributeName": "username", "KeyType": "HASH"}
        ],
        attribute_definitions=[
            {"AttributeName": "username", "AttributeType": "S"}
        ]
    )


def seed_test_data():
    """Seed the table with test data."""
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(TODO_TABLE_NAME)
    
    test_data = [
        {
            "user_id": "user1",
            "todo_id": str(uuid4()),
            "title": "Complete project documentation",
            "description": "Write comprehensive docs for the todo app",
            "completed": False,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        },
        {
            "user_id": "user1",
            "todo_id": str(uuid4()),
            "title": "Review code changes",
            "description": "Go through all recent PRs and provide feedback",
            "completed": True,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        },
        {
            "user_id": "user1",
            "todo_id": str(uuid4()),
            "title": "Setup CI/CD pipeline",
            "description": None,
            "completed": False,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        },
        {
            "user_id": "user2",
            "todo_id": str(uuid4()),
            "title": "Learn FastAPI",
            "description": "Complete FastAPI tutorial and build a sample app",
            "completed": False,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        },
        {
            "user_id": "user2",
            "todo_id": str(uuid4()),
            "title": "Deploy to production",
            "description": "Configure production environment and deploy",
            "completed": False,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
    ]
    
    print(f"Seeding test data into '{TODO_TABLE_NAME}'...")
    for item in test_data:
        try:
            table.put_item(Item=item)
            print(f"  ✓ Added todo: {item['title']}")
        except ClientError as e:
            print(f"  ✗ Error adding todo '{item['title']}': {e}")
    
    print(f"Test data seeding completed.")


def main():
    """Main function to initialize database."""
    print("Initializing DynamoDB...")
    
    # Create User table
    user_table_created = create_user_table()
    
    # Create Todo table
    todo_table_created = create_todo_table()
    
    if user_table_created and todo_table_created:
        seed_test_data()
        print("\nDatabase initialization completed successfully!")
    else:
        print("\nDatabase initialization failed!")


if __name__ == "__main__":
    main()

