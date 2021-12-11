from fastapi import APIRouter

from controllers.blockchain import BlockChain
from controllers.data import response, ResponseError

router = APIRouter()
blockchain = BlockChain()

def test_chain():
    if not blockchain.is_chain_valid():
        return response(ResponseError(status_code=409, fields={
                "status": "fail",
                "type": "Invalid Chain"
            }))


@router.post("/mine")
async def mine_block(data: str):
    test_chain()
    block = blockchain.mine(data)
    blockchain.chain.append(block)
    return block


@router.get("/chain")
async def get_chain():
    test_chain()
    return blockchain.chain

@router.get("/tail")
async def get_last_block():
    test_chain()
    return blockchain.get_previous_block()