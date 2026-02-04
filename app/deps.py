from fastapi import Header, HTTPException, status

def verify_rapidapi_key(x_rapidapi_key: str = Header(None)):
    if x_rapidapi_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-RapidAPI-Key header"
        )

    # Jangan cek nilainya, RapidAPI yang urus validasi user
    return True
