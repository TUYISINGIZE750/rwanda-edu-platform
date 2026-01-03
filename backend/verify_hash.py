import bcrypt

password = "dos12024"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(f"Correct hash for 'dos12024': {hashed.decode()}")

# Test the hash from SQL
sql_hash = "$2b$12$8g7aOs69f71yngUyR5v4iOwsBmNWbkolcKkeOnKhsaQFaagWZQqGy"
if bcrypt.checkpw(password.encode(), sql_hash.encode()):
    print("SQL hash is CORRECT")
else:
    print("SQL hash is WRONG")
