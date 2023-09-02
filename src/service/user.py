from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import bcrypt
import os

load_dotenv()


class UserService:
    encode: str = "UTF-8"
    secret_key: str = os.getenv("JWT_SECRET_KEY")
    algorithm: str = "HS256"

    def hash_password(self, password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(password.encode(self.encode), salt=bcrypt.gensalt())
        return hashed_password.decode(self.encode)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        request_password: bytes = password.encode(self.encode)
        hashed_password: bytes = hashed_password.encode(self.encode)
        return bcrypt.checkpw(request_password, hashed_password)

    def create_jwt(self, username: str, role: int) -> str:
        return jwt.encode(
            {
                "sub": f"{username},{role}",
                "exp": datetime.now() + timedelta(days=7)
            },
            key=self.secret_key,
            algorithm=self.algorithm,
        )

    def verify_token(self, access_token: str) -> str | None:
        try:
            payload: dict = jwt.decode(access_token, key=self.secret_key, algorithms=self.algorithm)
        except jwt.ExpiredSignatureError:
            return None

        return payload.get("sub")
