"""
Seed the database with test data
"""
import sys
from datetime import datetime, timedelta
from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.prompt import Prompt
from app.models.response import Response
from app.models.feedback import Feedback
from app.models.evaluation import Evaluation
from app.models.alert import Alert
from app.core.security import get_password_hash
import random

def seed_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Clear existing data
        print("Clearing existing data...")
        db.query(Feedback).delete()
        db.query(Evaluation).delete()
        db.query(Response).delete()
        db.query(Prompt).delete()
        db.query(Alert).delete()
        db.query(User).delete()
        db.commit()
        
        # Create test users
        print("Creating test users...")
        admin_user = User(
            email="admin@example.com",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            role="admin"
        )
        test_user = User(
            email="test@example.com",
            username="testuser",
            hashed_password=get_password_hash("test123"),
            role="user"
        )
        db.add(admin_user)
        db.add(test_user)
        db.commit()
        db.refresh(admin_user)
        db.refresh(test_user)
        
        print(f"✓ Created admin user: admin@example.com / admin123")
        print(f"✓ Created test user: test@example.com / test123")
        
        # Create sample prompts and responses
        print("Creating sample conversations...")
        sample_conversations = [
            ("What is machine learning?", "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed."),
            ("Explain neural networks", "Neural networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) organized in layers that process information."),
            ("What is NLP?", "Natural Language Processing (NLP) is a branch of AI that helps computers understand, interpret, and generate human language in a valuable way."),
            ("Tell me about transformers", "Transformers are a type of neural network architecture that uses self-attention mechanisms to process sequential data, revolutionizing NLP tasks."),
            ("What is RAG?", "RAG (Retrieval-Augmented Generation) combines information retrieval with text generation to provide more accurate and contextual responses."),
        ]
        
        models = ["mixtral-8x7b-32768", "llama2-70b-4096"]
        
        for i, (prompt_text, response_text) in enumerate(sample_conversations):
            user = test_user if i % 2 == 0 else admin_user
            model = random.choice(models)
            
            # Create prompt
            prompt = Prompt(
                user_id=user.id,
                content=prompt_text,
                model=model,
                temperature="0.7",
                max_tokens=1024,
                session_id=f"session_{i // 2}",
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 7))
            )
            db.add(prompt)
            db.flush()
            
            # Create response
            tokens = random.randint(100, 500)
            latency = random.uniform(500, 2500)
            cost = tokens * 0.00024 / 1000
            
            response = Response(
                prompt_id=prompt.id,
                user_id=user.id,
                content=response_text,
                model=model,
                tokens_used=tokens,
                prompt_tokens=tokens // 2,
                completion_tokens=tokens // 2,
                latency_ms=latency,
                cost=cost,
                is_error=False,
                session_id=prompt.session_id,
                created_at=prompt.created_at
            )
            db.add(response)
            db.flush()
            
            # Add feedback
            if random.random() > 0.3:  # 70% have feedback
                feedback = Feedback(
                    response_id=response.id,
                    user_id=user.id,
                    rating=random.randint(3, 5),
                    comment="Great response!" if random.random() > 0.5 else None,
                    created_at=response.created_at + timedelta(minutes=5)
                )
                db.add(feedback)
            
            # Add evaluation
            if random.random() > 0.4:  # 60% have evaluations
                evaluation = Evaluation(
                    response_id=response.id,
                    faithfulness=random.uniform(0.7, 0.95),
                    relevance=random.uniform(0.75, 0.98),
                    context_precision=random.uniform(0.7, 0.9),
                    context_recall=random.uniform(0.65, 0.9),
                    hallucination_risk=random.uniform(0.05, 0.25),
                    ragas_score=random.uniform(0.75, 0.92),
                    created_at=response.created_at + timedelta(minutes=1)
                )
                db.add(evaluation)
        
        db.commit()
        print(f"✓ Created {len(sample_conversations)} sample conversations")
        
        # Create alerts
        print("Creating sample alerts...")
        alerts = [
            ("latency", "high", "High latency detected: 3500ms", False),
            ("error", "medium", "Multiple API errors detected", True),
            ("cost", "high", "Daily cost threshold exceeded", False),
        ]
        
        for alert_type, severity, message, is_resolved in alerts:
            alert = Alert(
                type=alert_type,
                severity=severity,
                message=message,
                is_resolved=is_resolved,
                created_at=datetime.utcnow() - timedelta(hours=random.randint(1, 48))
            )
            db.add(alert)
        
        db.commit()
        print(f"✓ Created {len(alerts)} sample alerts")
        
        print("\n" + "="*60)
        print("✅ Database seeded successfully!")
        print("="*60)
        print("\nTest Accounts:")
        print("  Admin:  admin@example.com / admin123")
        print("  User:   test@example.com / test123")
        print("\nYou can now start the backend server!")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
