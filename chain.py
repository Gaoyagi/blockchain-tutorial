import json
from datetime import datetime
import hashlib


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.transactions = []

        self.newBlock(previous_hash=1, proof=100)

    #basically pythns way of denoting a getter or setter function, can be called w/o using ()
    @property
    def last_block(self):
        return self.chain[-1]

    #every block should contain: index, timestamp, transaction list, proof (curr hash), prev block hash
    def newBlock(self, previous_hash, proof):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),        #after previous block is compelted then you make the hash
            'transactions': self.transactions
        }

        self.transactions = []
        self.chain.append(block)
        return block

    #add a new transaction for a block
    def newTransaction(self, sender, recipient, amount):
        self.transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    #static methods: only 1 occurance for all the occruances of this class object, this alsmot means theydont mean a "Self" arg
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """This method is where you the consensus algorithm is implemented. It takes two parameters including self and last_proof"""
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof +=1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """This method validates the block"""
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

