"""
MongoDB Quick Summary - Show key metrics only
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "llmops")

def show_summary():
    try:
        client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
        db = client[MONGODB_DB_NAME]
        
        # Test connection
        client.server_info()
        
        print("\n" + "="*60)
        print("  📊 MONGODB SUMMARY - " + MONGODB_DB_NAME.upper())
        print("="*60)
        
        # Count documents
        users_count = db.users.count_documents({})
        conversations_count = db.conversations.count_documents({})
        messages_count = db.chat_messages.count_documents({})
        activity_count = db.user_activity.count_documents({})
        
        print(f"\n📈 Collections:")
        print(f"   Users:           {users_count:>6}")
        print(f"   Conversations:   {conversations_count:>6}")
        print(f"   Messages:        {messages_count:>6}")
        print(f"   Activity:        {activity_count:>6}")
        
        # Activity totals
        if activity_count > 0:
            activities = list(db.user_activity.find())
            total_chats = sum(a.get('chat_count', 0) for a in activities)
            total_uploads = sum(a.get('upload_count', 0) for a in activities)
            total_queries = sum(a.get('query_count', 0) for a in activities)
            total_tokens = sum(a.get('total_tokens', 0) for a in activities)
            total_cost = sum(a.get('total_cost', 0.0) for a in activities)
            
            print(f"\n💬 Activity Summary:")
            print(f"   Chat Requests:   {total_chats:>6}")
            print(f"   Uploads:         {total_uploads:>6}")
            print(f"   RAG Queries:     {total_queries:>6}")
            print(f"   Total Tokens:    {total_tokens:>6,}")
            print(f"   Total Cost:      ${total_cost:.6f}")
            
            # Model breakdown
            model_totals = {}
            for activity in activities:
                for model, stats in activity.get('model_usage', {}).items():
                    model_name = model.split('/')[-1][:25]
                    if model_name not in model_totals:
                        model_totals[model_name] = {'requests': 0, 'tokens': 0}
                    model_totals[model_name]['requests'] += stats.get('requests', 0)
                    model_totals[model_name]['tokens'] += stats.get('tokens', 0)
            
            if model_totals:
                print(f"\n🤖 Model Usage:")
                for model, stats in sorted(model_totals.items(), key=lambda x: x[1]['requests'], reverse=True):
                    print(f"   {model:<25} {stats['requests']:>4} req  {stats['tokens']:>6,} tokens")
        
        # Recent users
        recent_users = list(db.users.find().sort("created_at", -1).limit(3))
        if recent_users:
            print(f"\n👥 Recent Users:")
            for user in recent_users:
                print(f"   • {user['username']:<15} ({user['email']})")
        
        # Recent conversations
        recent_convs = list(db.conversations.find().sort("updated_at", -1).limit(3))
        if recent_convs:
            print(f"\n💭 Recent Conversations:")
            for conv in recent_convs:
                title = conv['title'][:40] + "..." if len(conv['title']) > 40 else conv['title']
                print(f"   • {title}")
        
        print("\n" + "="*60)
        print("  ✅ MongoDB is connected and has data!")
        print("="*60)
        print("\n💡 Run 'view_mongodb_data.py' for detailed view")
        print("💡 Run 'seed_mongodb.py' to add more sample data\n")
        
        client.close()
        
    except Exception as e:
        print("\n" + "="*60)
        print("  ❌ ERROR CONNECTING TO MONGODB")
        print("="*60)
        print(f"\n{str(e)}\n")
        print("Troubleshooting:")
        print("  1. Check if MongoDB is running")
        print("  2. Verify connection in .env file")
        print("  3. Run 'net start MongoDB' if service stopped\n")

if __name__ == "__main__":
    show_summary()
