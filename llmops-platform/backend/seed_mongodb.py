"""
Script to seed MongoDB with sample data
This populates the database with realistic test data for testing
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timedelta
import random
from passlib.context import CryptContext

# Load environment variables
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "llmops_db")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_mongodb():
    """Seed MongoDB with sample data"""
    print("=" * 60)
    print("🌱 Seeding MongoDB with Sample Data")
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
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        response = input("⚠️  Clear existing data? (y/N): ")
        if response.lower() == 'y':
            print("🗑️  Clearing existing collections...")
            db.users.delete_many({})
            db.conversations.delete_many({})
            db.chat_messages.delete_many({})
            db.user_activity.delete_many({})
            print("✅ Cleared existing data")
            print()
        
        # 1. Create Users
        print("👥 Creating users...")
        users = [
            {
                "email": "test@example.com",
                "username": "testuser",
                "password": pwd_context.hash("password123"),
                "role": "user",
                "is_active": True,
                "created_at": datetime.now() - timedelta(days=30)
            },
            {
                "email": "alice@example.com",
                "username": "alice",
                "password": pwd_context.hash("password123"),
                "role": "user",
                "is_active": True,
                "created_at": datetime.now() - timedelta(days=20)
            },
            {
                "email": "bob@example.com",
                "username": "bob",
                "password": pwd_context.hash("password123"),
                "role": "user",
                "is_active": True,
                "created_at": datetime.now() - timedelta(days=15)
            }
        ]
        
        user_results = db.users.insert_many(users)
        user_ids = [str(uid) for uid in user_results.inserted_ids]
        print(f"✅ Created {len(users)} users")
        print()
        
        # 2. Create Conversations
        print("💬 Creating conversations...")
        
        conversation_titles = [
            "Introduction to Machine Learning",
            "Python Best Practices",
            "Building REST APIs",
            "Docker Containerization",
            "Understanding Neural Networks",
            "Database Design Patterns",
            "Cloud Architecture Discussion",
            "React Component Patterns",
            "TypeScript Advanced Features",
            "Microservices vs Monoliths"
        ]
        
        conversations = []
        for i, title in enumerate(conversation_titles):
            user_id = user_ids[i % len(user_ids)]
            days_ago = random.randint(1, 30)
            conv = {
                "user_id": user_id,
                "title": title,
                "created_at": datetime.now() - timedelta(days=days_ago),
                "updated_at": datetime.now() - timedelta(days=days_ago - random.randint(0, 5)),
                "message_count": random.randint(4, 20)
            }
            conversations.append(conv)
        
        conv_results = db.conversations.insert_many(conversations)
        conv_ids = [str(cid) for cid in conv_results.inserted_ids]
        print(f"✅ Created {len(conversations)} conversations")
        print()
        
        # 3. Create Chat Messages
        print("💭 Creating chat messages...")
        
        sample_messages = [
            ("user", "What is machine learning?"),
            ("assistant", "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It uses algorithms and statistical models to analyze patterns in data."),
            ("user", "Can you explain supervised learning?"),
            ("assistant", "Supervised learning is a type of machine learning where the algorithm learns from labeled training data. It maps input data to output labels, learning the relationship between features and targets to make predictions on new, unseen data."),
            ("user", "How do I get started with Python?"),
            ("assistant", "To start with Python: 1) Install Python from python.org, 2) Learn basic syntax and data types, 3) Practice with simple programs, 4) Explore libraries like NumPy and Pandas, 5) Work on small projects to apply your knowledge."),
            ("user", "What's the difference between REST and GraphQL?"),
            ("assistant", "REST uses multiple endpoints for different resources with fixed data structures, while GraphQL uses a single endpoint where clients can request exactly the data they need. GraphQL provides more flexibility but adds complexity."),
            ("user", "Explain Docker containers"),
            ("assistant", "Docker containers are lightweight, standalone packages that include everything needed to run an application: code, runtime, system tools, libraries, and settings. They ensure consistency across development and production environments."),
        ]
        
        models = [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "meta-llama/llama-4-scout-17b-16e-instruct"
        ]
        
        messages = []
        for conv_id, conv in zip(conv_ids, conversations):
            user_id = conv["user_id"]
            msg_count = conv["message_count"]
            
            for i in range(msg_count):
                role = "user" if i % 2 == 0 else "assistant"
                sample_msg = sample_messages[i % len(sample_messages)]
                
                if sample_msg[0] == role:
                    content = sample_msg[1]
                else:
                    content = sample_messages[(i + 1) % len(sample_messages)][1]
                
                msg = {
                    "conversation_id": conv_id,
                    "user_id": user_id,
                    "role": role,
                    "content": content,
                    "timestamp": conv["created_at"] + timedelta(minutes=i * 2)
                }
                
                if role == "assistant":
                    model = random.choice(models)
                    tokens = random.randint(50, 500)
                    latency = random.uniform(500, 3000)
                    msg.update({
                        "model": model,
                        "tokens_used": tokens,
                        "latency_ms": round(latency, 2),
                        "cost": tokens * 0.0000002
                    })
                
                messages.append(msg)
        
        if messages:
            db.chat_messages.insert_many(messages)
            print(f"✅ Created {len(messages)} chat messages")
        print()
        
        # 4. Create User Activity
        print("📈 Creating user activity data...")
        
        for user_id in user_ids:
            # Get user's messages
            user_messages = [m for m in messages if m["user_id"] == user_id and m["role"] == "assistant"]
            
            total_tokens = sum(m.get("tokens_used", 0) for m in user_messages)
            total_cost = sum(m.get("cost", 0) for m in user_messages)
            latencies = [m.get("latency_ms", 0) for m in user_messages if m.get("latency_ms")]
            
            # Group by date
            requests_by_date = {}
            for msg in user_messages:
                date_key = msg["timestamp"].strftime("%Y-%m-%d")
                if date_key not in requests_by_date:
                    requests_by_date[date_key] = {
                        "requests": 0,
                        "tokens": 0,
                        "cost": 0.0,
                        "latencies": []
                    }
                requests_by_date[date_key]["requests"] += 1
                requests_by_date[date_key]["tokens"] += msg.get("tokens_used", 0)
                requests_by_date[date_key]["cost"] += msg.get("cost", 0)
                requests_by_date[date_key]["latencies"].append(msg.get("latency_ms", 0))
            
            # Group by model
            model_usage = {}
            for msg in user_messages:
                model = msg.get("model", "unknown")
                if model not in model_usage:
                    model_usage[model] = {
                        "requests": 0,
                        "tokens": 0,
                        "cost": 0.0,
                        "latencies": [],
                        "errors": 0
                    }
                model_usage[model]["requests"] += 1
                model_usage[model]["tokens"] += msg.get("tokens_used", 0)
                model_usage[model]["cost"] += msg.get("cost", 0)
                model_usage[model]["latencies"].append(msg.get("latency_ms", 0))
            
            activity = {
                "user_id": user_id,
                "chat_count": len(user_messages),
                "upload_count": random.randint(0, 5),
                "query_count": random.randint(0, 10),
                "total_tokens": total_tokens,
                "total_cost": total_cost,
                "requests_by_date": requests_by_date,
                "latencies": latencies[-1000:],  # Keep last 1000
                "model_usage": model_usage,
                "last_activity": datetime.now() - timedelta(days=random.randint(0, 5)),
                "created_at": datetime.now() - timedelta(days=30)
            }
            
            db.user_activity.insert_one(activity)
        
        print(f"✅ Created {len(user_ids)} user activity records")
        print()
        
        # Summary
        print("=" * 60)
        print("✅ Sample Data Seeding Complete!")
        print("=" * 60)
        print()
        print(f"👥 Users: {len(users)}")
        print(f"💬 Conversations: {len(conversations)}")
        print(f"💭 Messages: {len(messages)}")
        print(f"📈 User Activity: {len(user_ids)}")
        print()
        print("Login credentials:")
        print("  Email: test@example.com")
        print("  Password: password123")
        print()
        print("  Email: alice@example.com")
        print("  Password: password123")
        print()
        print("  Email: bob@example.com")
        print("  Password: password123")
        print()
        print("=" * 60)
        print()
        print("🔍 Next Steps:")
        print("1. Start MongoDB backend: python app/main_mongo.py")
        print("2. Login at http://localhost:3000")
        print("3. View conversations and messages")
        print("4. Check dashboard analytics")
        print("5. Run: python verify_mongodb.py to verify data")
        print()
        
    except Exception as e:
        print(f"❌ Error seeding MongoDB: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    seed_mongodb()
