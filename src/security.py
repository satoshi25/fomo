from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException


def get_access_token(
    auth_header: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False))
) -> str:

    if not auth_header:
        raise HTTPException(status_code=401, detail="Not Authorized")

    return auth_header.credentials
