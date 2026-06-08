"""
Test PostgreSQL connection
"""
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("="*60)
print("🔍 Testing PostgreSQL Connection")
print("="*60)
print(f"\n📍 Database URL: {DATABASE_URL[:50]}...")

try:
    # Create engine
    print("\n⏳ Creating database engine...")
    engine = create_engine(DATABASE_URL)
    
    # Test connection
    print("⏳ Attempting to connect...")
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        
        print("\n✅ Connection Successful!")
        print(f"\n📊 PostgreSQL Version:")
        print(f"   {version[:80]}...")
        
        # Test basic queries
        print("\n⏳ Testing basic operations...")
        
        # Check if we can create tables
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS connection_test (
                id SERIAL PRIMARY KEY,
                test_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        connection.commit()
        
        # Insert test data
        connection.execute(text("""
            INSERT INTO connection_test (test_message) 
            VALUES ('Connection test successful!');
        """))
        connection.commit()
        
        # Query test data
        result = connection.execute(text("""
            SELECT COUNT(*) FROM connection_test;
        """))
        count = result.fetchone()[0]
        
        # Clean up test table
        connection.execute(text("DROP TABLE IF EXISTS connection_test;"))
        connection.commit()
        
        print(f"✅ Basic operations successful!")
        print(f"   - Created table")
        print(f"   - Inserted data")
        print(f"   - Queried data (found {count} rows)")
        print(f"   - Dropped test table")
        
        print("\n" + "="*60)
        print("✅ PostgreSQL Connection Verified!")
        print("="*60)
        print("\n✨ Your database is ready for the LLMOps platform!")
        print("="*60)
        
except Exception as e:
    print("\n" + "="*60)
    print("❌ Connection Failed!")
    print("="*60)
    print(f"\nError: {str(e)}")
    print("\n🔧 Troubleshooting:")
    print("   1. Check if DATABASE_URL is correct in .env")
    print("   2. Verify network connection to database")
    print("   3. Ensure database credentials are valid")
    print("   4. Check if database server is running")
    print("="*60)
    sys.exit(1)
