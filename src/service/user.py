import bcrypt


class UserService:
    encode: str = "UTF-8"

    def hash_password(self, password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(password.encode(self.encode), salt=bcrypt.gensalt())
        return hashed_password.decode(self.encode)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        request_password: bytes = password.encode(self.encode)
        hashed_password: bytes = hashed_password.encode(self.encode)
        return bcrypt.checkpw(request_password, hashed_password)
