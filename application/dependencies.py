from fastapi import Header, HTTPException


async def header_token(x_token: str = Header(...)):
    if x_token != '':
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def query_token(token: str):
    if token is not None:
        raise HTTPException(status_code=400, detail="Token query invalid")