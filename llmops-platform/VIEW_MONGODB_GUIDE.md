# 📊 How to View MongoDB Data

## ✅ Current Data in MongoDB

Your MongoDB database **`llmops`** contains:
- **3 Users** (testuser, alice, bob)
- **10 Conversations** with various topics
- **3 User Activity Records** tracking usage across all models
- **16,334 Total Tokens Used**
- **$0.003267 Total Cost**

---

## 🔍 Method 1: Python Script (Easiest)

### View All Data:
```bash
cd backend
venv\Scripts\python.exe view_mongodb_data.py
```

This shows:
- ✅ All users with details
- ✅ All conversations with message counts
- ✅ All messages grouped by conversation
- ✅ User activity with model usage breakdown
- ✅ Summary statistics

---

## 🖥️ Method 2: MongoDB Compass (GUI)

**MongoDB Compass** is the official visual tool for MongoDB.

### Steps:
1. **Download**: https://www.mongodb.com/try/download/compass
2. **Install** MongoDB Compass
3. **Connect**: 
   - Connection String: `mongodb://localhost:27017`
   - Click "Connect"
4. **Navigate**:
   - Database: `llmops`
   - Collections: `users`, `conversations`, `chat_messages`, `user_activity`

### Benefits:
- 🎨 Visual interface
- 🔍 Easy filtering and searching
- 📊 Aggregation pipelines
- 📝 Edit documents directly
- 📈 Schema analysis

---

## 💻 Method 3: MongoDB Shell (mongosh)

### Install mongosh:
```bash
# Download from: https://www.mongodb.com/try/download/shell
# Or via package manager
```

### Connect and View:
```bash
# Connect
mongosh mongodb://localhost:27017

# Switch to database
use llmops

# View collections
show collections

# View users
db.users.find().pretty()

# View conversations
db.conversations.find().pretty()

# View user activity
db.user_activity.find().pretty()

# Count documents
db.users.countDocuments()
db.conversations.countDocuments()

# Find specific user
db.users.findOne({email: "test@example.com"})

# View latest conversations
db.conversations.find().sort({updated_at: -1}).limit(5).pretty()

# Exit
exit
```

---

## 📋 Method 4: Quick Python Queries

### Create Custom Query Script:

Create `query_mongodb.py`:
```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["llmops"]

# Query users
print("Users:")
for user in db.users.find():
    print(f"  {user['username']} - {user['email']}")

# Query conversations
print("\nRecent Conversations:")
for conv in db.conversations.find().sort("updated_at", -1).limit(5):
    print(f"  {conv['title']} ({conv['message_count']} messages)")

# Query activity
print("\nUser Activity:")
for activity in db.user_activity.find():
    print(f"  User {activity['user_id']}: {activity['chat_count']} chats, {activity['total_tokens']} tokens")

client.close()
```

Run:
```bash
cd backend
venv\Scripts\python.exe query_mongodb.py
```

---

## 🎯 Common Queries

### View Specific User Data:
```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["llmops"]

# Find user by email
user = db.users.find_one({"email": "test@example.com"})
print(f"User: {user['username']}")
print(f"ID: {user['_id']}")

# Get user's conversations
user_id = user['_id']
conversations = db.conversations.find({"user_id": user_id})
for conv in conversations:
    print(f"  - {conv['title']}")

# Get user's activity
activity = db.user_activity.find_one({"user_id": user_id})
print(f"Chat count: {activity['chat_count']}")
print(f"Total tokens: {activity['total_tokens']}")

client.close()
```

### View Model Usage Statistics:
```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["llmops"]

# Aggregate model usage across all users
activities = db.user_activity.find()

model_stats = {}
for activity in activities:
    for model, stats in activity.get('model_usage', {}).items():
        if model not in model_stats:
            model_stats[model] = {'requests': 0, 'tokens': 0}
        model_stats[model]['requests'] += stats['requests']
        model_stats[model]['tokens'] += stats['tokens']

print("Model Usage Across All Users:")
for model, stats in model_stats.items():
    print(f"  {model}:")
    print(f"    Requests: {stats['requests']}")
    print(f"    Tokens: {stats['tokens']}")

client.close()
```

---

## 📊 Your Current Data Summary

Based on the script output:

### Users (3):
1. **testuser** (test@example.com)
   - 22 chats, 5 uploads, 7 RAG queries
   - 6,492 tokens used ($0.001298)
   - Uses all 3 models

2. **alice** (alice@example.com)
   - 19 chats, 5 uploads, 5 RAG queries
   - 6,289 tokens used ($0.001258)
   - Uses all 3 models

3. **bob** (bob@example.com)
   - 13 chats, 5 uploads, 3 RAG queries
   - 3,553 tokens used ($0.000711)
   - Uses all 3 models

### Conversations (10):
- Introduction to Machine Learning (11 messages)
- Python Best Practices (17 messages)
- Building REST APIs (14 messages)
- Docker Containerization (17 messages)
- Understanding Neural Networks (17 messages)
- Database Design Patterns (7 messages)
- Cloud Architecture Discussion (14 messages)
- React Component Patterns (7 messages)
- TypeScript Advanced Features (7 messages)
- Microservices vs Monoliths (5 messages)

### Model Usage:
- **Llama 4 Scout 17B**: 20 requests, 5,909 tokens
- **Llama 3.3 70B**: 16 requests, 4,604 tokens  
- **Llama 3.1 8B**: 18 requests, 5,821 tokens

### Total Statistics:
- 54 total chat requests
- 15 document uploads
- 15 RAG queries
- 16,334 tokens used
- $0.003267 total cost

---

## 🔧 Useful MongoDB Commands

### Backup Database:
```bash
mongodump --db llmops --out ./mongodb_backup
```

### Restore Database:
```bash
mongorestore --db llmops ./mongodb_backup/llmops
```

### Export Collection to JSON:
```bash
mongoexport --db llmops --collection users --out users.json --pretty
```

### Import JSON to Collection:
```bash
mongoimport --db llmops --collection users --file users.json
```

### Clear All Data (DANGER!):
```bash
mongosh
use llmops
db.users.deleteMany({})
db.conversations.deleteMany({})
db.chat_messages.deleteMany({})
db.user_activity.deleteMany({})
```

---

## 🚀 Integration with Application

### Current Status:
- ⚠️ **Application is using**: `main_simple.py` (in-memory storage)
- 💾 **MongoDB has**: Sample seed data from previous run
- 🔄 **To use MongoDB**: Switch to `main_mongo.py`

### Switch to MongoDB Backend:

**Stop current backend**:
```bash
# Find the process
tasklist | findstr python

# Kill it or use Ctrl+C in terminal
```

**Start MongoDB-enabled backend**:
```bash
cd backend
venv\Scripts\python.exe app/main_mongo.py
```

Now all new chats, uploads, and queries will be stored in MongoDB persistently!

---

## 📝 Create New Sample Data

If you want to add more test data:

```bash
cd backend
venv\Scripts\python.exe seed_mongodb.py
```

This adds:
- 3 users (if not exists)
- 10 conversations with various topics
- 116 messages across conversations
- 3 user activity records with model usage

---

## 🎯 Quick Access Commands

### View Data:
```bash
cd backend
venv\Scripts\python.exe view_mongodb_data.py
```

### Add Sample Data:
```bash
cd backend
venv\Scripts\python.exe seed_mongodb.py
```

### Verify MongoDB Connection:
```bash
cd backend
venv\Scripts\python.exe verify_mongodb.py
```

### Start MongoDB Backend:
```bash
cd backend
venv\Scripts\python.exe app/main_mongo.py
```

---

## 🐛 Troubleshooting

### MongoDB Not Running:
```bash
# Check if MongoDB service is running
sc query MongoDB

# Start MongoDB service
net start MongoDB
```

### Connection Issues:
- Verify `MONGODB_URL` in `.env`: `mongodb://localhost:27017`
- Verify `MONGODB_DB_NAME` in `.env`: `llmops`
- Check MongoDB is listening on port 27017

### No Data Showing:
- Run seed script: `python seed_mongodb.py`
- Check you're using the correct database name
- Verify collections exist: `db.getCollectionNames()` in mongosh

---

## 📚 Resources

- **MongoDB Compass**: https://www.mongodb.com/try/download/compass
- **MongoDB Shell**: https://www.mongodb.com/try/download/shell
- **PyMongo Docs**: https://pymongo.readthedocs.io/
- **MongoDB Manual**: https://docs.mongodb.com/manual/

---

## ✨ Recommendation

For the best experience viewing and managing MongoDB data:

1. **Install MongoDB Compass** (GUI) - Best for exploration and analysis
2. **Use `view_mongodb_data.py`** - Quick terminal view of all data
3. **Learn mongosh basics** - For quick queries and automation

All three methods work with your current setup! 🚀
