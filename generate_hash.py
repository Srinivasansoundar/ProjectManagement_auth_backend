from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Generate hashed password
password = input("Enter password: ")
hashed_password = pwd_context.hash(password)

# Generate UUID for admin
admin_id = uuid.uuid4()

print(f"\nAdmin ID (UUID): {admin_id}")
print(f"Hashed Password: {hashed_password}")