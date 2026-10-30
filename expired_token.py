import jwt
from datetime import datetime, timezone, timedelta

secret = "1982"

payload = {
    "sub": "student",
    "role": "student",
    "exp": datetime.now(timezone.utc) - timedelta(minutes=1)
}

token = jwt.encode(payload, secret, algorithm="HS256")

print(token)