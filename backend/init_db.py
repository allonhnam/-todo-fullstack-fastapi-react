"""
Initialize DynamoDB table and seed test data.
"""
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from uuid import uuid4
import os
from dotenv import load_dotenv
from models import TABLE_NAME, TABLE_SCHEMA, AWS_REGION

# Load environment variables from .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))


def get_dynamodb_client():
    """Get DynamoDB client configured with AWS credentials."""
    return boto3.client(
        "dynamodb",
        region_name=AWS_REGION,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )


def get_dynamodb_resource():
    """Get DynamoDB resource configured with AWS credentials."""
    return boto3.resource(
        "dynamodb",
        region_name=AWS_REGION,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )


def create_table_if_not_exists():
    """Create the todos table if it doesn't exist."""
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
                dynamodb_client.create_table(**TABLE_SCHEMA)
                
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


def seed_test_data():
    """Seed the table with test data."""
    dynamodb = get_dynamodb_resource()
    table = dynamodb.Table(TABLE_NAME)
    
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
    
    print(f"Seeding test data into '{TABLE_NAME}'...")
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
    
    if create_table_if_not_exists():
        seed_test_data()
        print("\nDatabase initialization completed successfully!")
    else:
        print("\nDatabase initialization failed!")


if __name__ == "__main__":
    main()

