from fastapi import Header, HTTPException, status

RAPIDAPI_KEY = "123456"

def verify_rapidapi_key(x_rapidapi_key: str = Header(None)):
    if x_rapidapi_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-RapidAPI-Key header"
        )
    if x_rapidapi_key != RAPIDAPI_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid RapidAPI Key"
        )
    return True
