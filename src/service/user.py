import bcrypt


class UserService:
    encode: str = "UTF-8"

    def hash_password(self, password: str) -> str:
        hashed_password: bytes = bcrypt.hashpw(password.encode(self.encode), salt=bcrypt.gensalt())
        return hashed_password.decode(self.encode)
