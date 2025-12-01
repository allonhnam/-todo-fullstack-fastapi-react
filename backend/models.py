"""
PynamoDB models for the todo application.
"""
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, BooleanAttribute, UTCDateTimeAttribute
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))


class User(Model):
    """User model using PynamoDB."""
    class Meta:
        table_name = "User"
        region = os.getenv("AWS_REGION", "us-east-1")
        aws_access_key_id = os.getenv("MY_AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("MY_AWS_SECRET_ACCESS_KEY")
    
    username = UnicodeAttribute(hash_key=True)
    hashed_password = UnicodeAttribute()


class Todo(Model):
    """Todo model using PynamoDB."""
    class Meta:
        table_name = "Todo"
        region = os.getenv("AWS_REGION", "us-east-1")
        aws_access_key_id = os.getenv("MY_AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("MY_AWS_SECRET_ACCESS_KEY")
    
    user_id = UnicodeAttribute(hash_key=True)
    todo_id = UnicodeAttribute(range_key=True)
    title = UnicodeAttribute()
    description = UnicodeAttribute(null=True)
    completed = BooleanAttribute(default=False)
    created_at = UTCDateTimeAttribute()
    updated_at = UTCDateTimeAttribute()

