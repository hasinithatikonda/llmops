"""
Script to verify MongoDB data storage
Run this to check if data is being stored in MongoDB
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import json

# Load environment variables
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "llmops_db")

def verify_mongodb():
    """Verify MongoDB connection and data"""
    print("=" * 60)
    print("🔍 MongoDB Data Verification")
    print("=" * 60)
    print()
    
    try:
        # Connect to MongoDB
        print(f"📡 Connecting to MongoDB at: {MONGODB_URL}")
        client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
        
        # Test connection
        client.admin.command('ping')
        print("✅ Connected to MongoDB successfully!")
        print()
        
        # Get database
        db = client[MONGODB_DB_NAME]
        print(f"📁 Using database: {MONGODB_DB_NAME}")
        print()
        
        # Check collections
        collections = db.list_collection_names()
        print(f"📚 Collections found: {len(collections)}")
        if collections:
            for coll in collections:
                print(f"   • {coll}")
        else:
            print("   ⚠️  No collections created yet")
        print()
        
        # Check each collection
        total_documents = 0
        
        print("=" * 60)
        print("📊 Collection Statistics")
        print("=" * 60)
        print()
        
        # Users Collection
        if "users" in collections:
            users_count = db.users.count_documents({})
            total_documents += users_count
            print(f"👥 users: {users_count} documents")
            if users_count > 0:
                latest_user = db.users.find_one(sort=[("created_at", -1)])
                if latest_user:
                    print(f"   Latest: {latest_user.get('email', 'N/A')} (created: {latest_user.get('created_at', 'N/A')})")
            print()
        
        # Conversations Collection
        if "conversations" in collections:
            convs_count = db.conversations.count_documents({})
            total_documents += convs_count
            print(f"💬 conversations: {convs_count} documents")
            if convs_count > 0:
                latest_conv = db.conversations.find_one(sort=[("created_at", -1)])
                if latest_conv:
                    print(f"   Latest: \"{latest_conv.get('title', 'Untitled')}\" (created: {latest_conv.get('created_at', 'N/A')})")
                    print(f"   Messages: {latest_conv.get('message_count', 0)}")
            print()
        
        # Chat Messages Collection
        if "chat_messages" in collections:
            msgs_count = db.chat_messages.count_documents({})
            total_documents += msgs_count
            print(f"💭 chat_messages: {msgs_count} documents")
            if msgs_count > 0:
                user_msgs = db.chat_messages.count_documents({"role": "user"})
                assistant_msgs = db.chat_messages.count_documents({"role": "assistant"})
                print(f"   User messages: {user_msgs}")
                print(f"   Assistant messages: {assistant_msgs}")
                latest_msg = db.chat_messages.find_one(sort=[("timestamp", -1)])
                if latest_msg:
                    content_preview = latest_msg.get('content', '')[:50] + "..." if len(latest_msg.get('content', '')) > 50 else latest_msg.get('content', '')
                    print(f"   Latest: \"{content_preview}\"")
                    print(f"   Model: {latest_msg.get('model', 'N/A')}")
                    print(f"   Tokens: {latest_msg.get('tokens_used', 0)}")
            print()
        
        # User Activity Collection
        if "user_activity" in collections:
            activity_count = db.user_activity.count_documents({})
            total_documents += activity_count
            print(f"📈 user_activity: {activity_count} documents")
            if activity_count > 0:
                for activity in db.user_activity.find():
                    print(f"   User ID: {activity.get('user_id', 'N/A')}")
                    print(f"   Chat count: {activity.get('chat_count', 0)}")
                    print(f"   Total tokens: {activity.get('total_tokens', 0):,}")
                    print(f"   Total cost: ${activity.get('total_cost', 0):.6f}")
                    print(f"   Last activity: {activity.get('last_activity', 'N/A')}")
                    
                    # Model usage breakdown
                    model_usage = activity.get('model_usage', {})
                    if model_usage:
                        print(f"   Models used: {len(model_usage)}")
                        for model, stats in model_usage.items():
                            print(f"      • {model}: {stats.get('requests', 0)} requests, {stats.get('tokens', 0)} tokens")
                    print()
            print()
        
        # Metrics Collection
        if "metrics" in collections:
            metrics_count = db.metrics.count_documents({})
            total_documents += metrics_count
            print(f"📊 metrics: {metrics_count} documents")
            print()
        
        # Evaluations Collection
        if "evaluations" in collections:
            eval_count = db.evaluations.count_documents({})
            total_documents += eval_count
            print(f"⭐ evaluations: {eval_count} documents")
            print()
        
        # Summary
        print("=" * 60)
        print("📈 Summary")
        print("=" * 60)
        print(f"Total Collections: {len(collections)}")
        print(f"Total Documents: {total_documents}")
        print()
        
        if total_documents == 0:
            print("⚠️  No data found in MongoDB!")
            print()
            print("Possible reasons:")
            print("1. Backend is using main_simple.py (in-memory storage)")
            print("2. No chat interactions performed yet")
            print("3. MongoDB connection is working but data not being saved")
            print()
            print("To fix:")
            print("1. Switch to MongoDB backend: python app/main_mongo.py")
            print("2. Or check if current backend is configured for MongoDB")
            print("3. Perform some chat interactions")
        else:
            print("✅ MongoDB is storing data successfully!")
            print()
            print("Data is being persisted and can be:")
            print("   • Viewed in MongoDB Compass")
            print("   • Queried via MongoDB shell")
            print("   • Accessed via API endpoints")
            print("   • Backed up and restored")
        
        print()
        print("=" * 60)
        
        # Sample queries
        if total_documents > 0:
            print()
            print("🔍 Sample Queries You Can Run:")
            print("=" * 60)
            print()
            print("# Get all conversations")
            print(f"db.conversations.find()")
            print()
            print("# Get messages for a conversation")
            print(f"db.chat_messages.find({{conversation_id: 'YOUR_CONV_ID'}})")
            print()
            print("# Get user activity stats")
            print(f"db.user_activity.find()")
            print()
            print("# Count total messages")
            print(f"db.chat_messages.countDocuments()")
            print()
        
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        print()
        print("Troubleshooting:")
        print("1. Check if MongoDB is running")
        print("2. Verify MONGODB_URL in .env file")
        print("3. Check network/firewall settings")
        print("4. For Atlas: Verify IP whitelist and credentials")
        print()
        return False
    
    return True

if __name__ == "__main__":
    verify_mongodb()
