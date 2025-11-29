"""
DynamoDB table models for the todo application.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Todo(BaseModel):
    """Todo item model."""
    user_id: str = Field(..., description="Partition key - user identifier")
    todo_id: UUID = Field(default_factory=uuid4, description="Sort key - unique todo identifier")
    title: str = Field(..., description="Todo title")
    description: Optional[str] = Field(None, description="Todo description")
    completed: bool = Field(default=False, description="Completion status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    class Config:
        json_encoders = {
            UUID: str,
            datetime: lambda v: v.isoformat()
        }


# DynamoDB configuration
TABLE_NAME = "Todo"
AWS_REGION = "us-east-1"

# DynamoDB table schema definition
TABLE_SCHEMA = {
    "TableName": TABLE_NAME,
    "KeySchema": [
        {
            "AttributeName": "user_id",
            "KeyType": "HASH"  # Partition key
        },
        {
            "AttributeName": "todo_id",
            "KeyType": "RANGE"  # Sort key
        }
    ],
    "AttributeDefinitions": [
        {
            "AttributeName": "user_id",
            "AttributeType": "S"  # String
        },
        {
            "AttributeName": "todo_id",
            "AttributeType": "S"  # String (UUID stored as string)
        }
    ],
    "BillingMode": "PAY_PER_REQUEST"  # On-demand billing
}

