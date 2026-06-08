from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# The static hash we're using
STATIC_HASH = "$2b$12$j/.4hR277RAP2JED8yW2m.TxQ1p0Ftbe6QmIl1s8M.xqEXpnyeBX2"

print("Testing password verification:")
print(f"Password: password123")
print(f"Hash: {STATIC_HASH}")

result = pwd_context.verify("password123", STATIC_HASH)
print(f"Verification result: {result}")

if result:
    print("✅ Password verification WORKS!")
else:
    print("❌ Password verification FAILED!")
