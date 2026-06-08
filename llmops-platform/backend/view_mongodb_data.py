"""
View MongoDB Data - LLMOps Platform
Shows all data stored in the llmops database
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import json

# Load environment variables
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "llmops")

def print_separator(title=""):
    """Print a nice separator"""
    print("\n" + "=" * 80)
    if title:
        print(f"  {title}")
        print("=" * 80)

def format_datetime(dt):
    """Format datetime for display"""
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return str(dt)

def view_mongodb_data():
    """View all data in MongoDB"""
    try:
        # Connect to MongoDB
        print(f"Connecting to MongoDB at {MONGODB_URL}...")
        client = MongoClient(MONGODB_URL)
        db = client[MONGODB_DB_NAME]
        
        # Test connection
        client.server_info()
        print(f"✅ Connected successfully to database: '{MONGODB_DB_NAME}'")
        
        # Get all collections
        collections = db.list_collection_names()
        print(f"\n📊 Found {len(collections)} collections: {', '.join(collections)}")
        
        # View Users
        print_separator("👥 USERS")
        users = list(db.users.find())
        print(f"Total users: {len(users)}\n")
        for i, user in enumerate(users, 1):
            print(f"{i}. {user.get('username')} ({user.get('email')})")
            print(f"   ID: {user.get('_id')}")
            print(f"   Role: {user.get('role')}")
            print(f"   Active: {user.get('is_active')}")
            print(f"   Created: {format_datetime(user.get('created_at'))}")
            print()
        
        # View Conversations
        print_separator("💬 CONVERSATIONS")
        conversations = list(db.conversations.find())
        print(f"Total conversations: {len(conversations)}\n")
        for i, conv in enumerate(conversations, 1):
            print(f"{i}. Conversation ID: {conv.get('conversation_id')}")
            print(f"   User ID: {conv.get('user_id')}")
            print(f"   Title: {conv.get('title')}")
            print(f"   Model: {conv.get('model', 'N/A')}")
            print(f"   Messages: {conv.get('message_count', 0)}")
            print(f"   Created: {format_datetime(conv.get('created_at'))}")
            print(f"   Updated: {format_datetime(conv.get('updated_at'))}")
            print()
        
        # View Messages
        print_separator("📨 MESSAGES")
        messages = list(db.messages.find().sort("timestamp", 1))
        print(f"Total messages: {len(messages)}\n")
        
        # Group messages by conversation
        messages_by_conv = {}
        for msg in messages:
            conv_id = msg.get('conversation_id')
            if conv_id not in messages_by_conv:
                messages_by_conv[conv_id] = []
            messages_by_conv[conv_id].append(msg)
        
        for conv_id, msgs in messages_by_conv.items():
            print(f"Conversation: {conv_id}")
            print(f"{'─' * 60}")
            for msg in msgs:
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')
                # Truncate long messages
                if len(content) > 100:
                    content = content[:97] + "..."
                print(f"  [{role.upper()}]: {content}")
                if msg.get('tokens_used'):
                    print(f"  Tokens: {msg.get('tokens_used')}, Latency: {msg.get('latency_ms')}ms")
                print(f"  Time: {format_datetime(msg.get('timestamp'))}")
                print()
            print()
        
        # View User Activity
        print_separator("📊 USER ACTIVITY")
        activities = list(db.user_activity.find())
        print(f"Total activity records: {len(activities)}\n")
        for i, activity in enumerate(activities, 1):
            print(f"{i}. User ID: {activity.get('user_id')}")
            print(f"   Chat Count: {activity.get('chat_count', 0)}")
            print(f"   Upload Count: {activity.get('upload_count', 0)}")
            print(f"   Query Count: {activity.get('query_count', 0)}")
            print(f"   Total Tokens: {activity.get('total_tokens', 0)}")
            print(f"   Total Cost: ${activity.get('total_cost', 0.0):.6f}")
            print(f"   Last Activity: {format_datetime(activity.get('last_activity'))}")
            
            # Show model usage
            model_usage = activity.get('model_usage', {})
            if model_usage:
                print(f"   Models Used:")
                for model, stats in model_usage.items():
                    model_short = model.split('/')[-1][:30]
                    print(f"     • {model_short}: {stats.get('requests', 0)} requests, {stats.get('tokens', 0)} tokens")
            print()
        
        # Summary Statistics
        print_separator("📈 SUMMARY STATISTICS")
        total_users = len(users)
        total_conversations = len(conversations)
        total_messages = len(messages)
        total_activity = len(activities)
        
        # Calculate totals
        total_tokens = sum(a.get('total_tokens', 0) for a in activities)
        total_cost = sum(a.get('total_cost', 0.0) for a in activities)
        total_chats = sum(a.get('chat_count', 0) for a in activities)
        total_uploads = sum(a.get('upload_count', 0) for a in activities)
        total_queries = sum(a.get('query_count', 0) for a in activities)
        
        print(f"\n{'Metric':<30} {'Count':>15}")
        print("─" * 45)
        print(f"{'Users':<30} {total_users:>15}")
        print(f"{'Conversations':<30} {total_conversations:>15}")
        print(f"{'Messages':<30} {total_messages:>15}")
        print(f"{'Activity Records':<30} {total_activity:>15}")
        print(f"{'Total Chat Requests':<30} {total_chats:>15}")
        print(f"{'Total Document Uploads':<30} {total_uploads:>15}")
        print(f"{'Total RAG Queries':<30} {total_queries:>15}")
        print(f"{'Total Tokens Used':<30} {total_tokens:>15,}")
        print(f"{'Total Cost':<30} ${total_cost:>14.6f}")
        
        print_separator()
        print("✅ Data retrieval complete!")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Ensure MongoDB is running: Check if service is started")
        print("2. Check connection URL in .env file")
        print("3. Verify database name is correct")
        print("4. Run: python seed_mongodb.py (if no data)")

if __name__ == "__main__":
    print("\n🔍 MongoDB Data Viewer - LLMOps Platform")
    view_mongodb_data()
