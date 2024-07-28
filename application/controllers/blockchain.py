import datetime
import hashlib
import json


class BlockChain:
    def __init__(self) -> None:
        self.chain = list()
        genesis_block = self._create_block('Genesis Block')
        self.chain.append(genesis_block)
        ...

    def _create_block(self, data: str, proof: int = 0, hash_previous: str = "0") -> dict:
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'data': data,
            'proof': proof,
            'hash_previous': hash_previous
        }
        return block

    def _hash(self, block: dict) -> str:
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def mine(self, data) -> int:
        new_block = None
        while  not self._validate_proof(new_block):
            proof = new_block["proof"]+1 if new_block else 0
            new_block = self._create_block(data, proof, self._hash(self.get_previous_block()))
        return new_block

    def _validate_proof(self, block: dict, difficult: int = 3) -> bool:
        return (self._hash(block)[0:difficult] == "0" * difficult) #and self._hash(block)[-difficult:] == "0" * difficult)

    def get_previous_block(self) -> dict:
        return self.chain[-1]

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            if self.chain[i]["hash_previous"] != self._hash(self.chain[i-1]) or not self._validate_proof(self.chain[i]):
                return False
        return True

if __name__ == "__main__":
    a = BlockChain()
    new_block = a.mine({})
    a.chain.append(new_block)
    print(a.chain)
    print("last_hash:", a._hash(a.get_previous_block()))
    print("valid:", a.is_chain_valid())
