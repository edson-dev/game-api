from fastapi import Header, HTTPException


async def header_token(token: str = Header(...)):
    if not token:
        raise HTTPException(status_code=400, detail="Token header invalid")


async def query_token(token: str):
    if not token:
        raise HTTPException(status_code=400, detail="Token query invalid")