"""
MongoDB Database Configuration and Connection
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os
from typing import Optional

# MongoDB Configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "llmops_db")

# Async MongoDB client for FastAPI
async_client: Optional[AsyncIOMotorClient] = None
async_db = None

# Sync MongoDB client for non-async operations
sync_client: Optional[MongoClient] = None
sync_db = None

def get_mongodb_client():
    """Get synchronous MongoDB client"""
    global sync_client, sync_db
    if sync_client is None:
        sync_client = MongoClient(MONGODB_URL)
        sync_db = sync_client[MONGODB_DB_NAME]
    return sync_db

async def connect_to_mongodb():
    """Connect to MongoDB on application startup"""
    global async_client, async_db
    async_client = AsyncIOMotorClient(MONGODB_URL)
    async_db = async_client[MONGODB_DB_NAME]
    
    # Test connection
    try:
        await async_client.admin.command('ping')
        print(f"✅ Connected to MongoDB at {MONGODB_URL}")
        print(f"📁 Using database: {MONGODB_DB_NAME}")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        print(f"⚠️  Make sure MongoDB is running on {MONGODB_URL}")

async def close_mongodb_connection():
    """Close MongoDB connection on application shutdown"""
    global async_client
    if async_client:
        async_client.close()
        print("🔌 Closed MongoDB connection")

def get_database():
    """Get async MongoDB database instance"""
    return async_db

# Collection names
COLLECTIONS = {
    "users": "users",
    "chat_messages": "chat_messages",
    "conversations": "conversations",
    "user_activity": "user_activity",
    "metrics": "metrics",
    "evaluations": "evaluations",
}

async def init_collections():
    """Initialize MongoDB collections with indexes"""
    if async_db is None:
        return
    
    try:
        # Users collection indexes
        await async_db[COLLECTIONS["users"]].create_index("email", unique=True)
        await async_db[COLLECTIONS["users"]].create_index("username")
        
        # Chat messages indexes
        await async_db[COLLECTIONS["chat_messages"]].create_index("user_id")
        await async_db[COLLECTIONS["chat_messages"]].create_index("conversation_id")
        await async_db[COLLECTIONS["chat_messages"]].create_index("timestamp")
        await async_db[COLLECTIONS["chat_messages"]].create_index([("user_id", 1), ("timestamp", -1)])
        
        # Conversations indexes
        await async_db[COLLECTIONS["conversations"]].create_index("user_id")
        await async_db[COLLECTIONS["conversations"]].create_index("created_at")
        await async_db[COLLECTIONS["conversations"]].create_index([("user_id", 1), ("created_at", -1)])
        
        # User activity indexes
        await async_db[COLLECTIONS["user_activity"]].create_index("user_id", unique=True)
        await async_db[COLLECTIONS["user_activity"]].create_index("last_activity")
        
        # Metrics indexes
        await async_db[COLLECTIONS["metrics"]].create_index("user_id")
        await async_db[COLLECTIONS["metrics"]].create_index("date")
        await async_db[COLLECTIONS["metrics"]].create_index([("user_id", 1), ("date", -1)])
        
        print("✅ MongoDB collections and indexes initialized")
    except Exception as e:
        print(f"⚠️  Error initializing collections: {e}")
