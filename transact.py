import hashlib
import time

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = (
            str(self.sender)
            + str(self.recipient)
            + str(self.amount)
            + str(self.timestamp)
        )
        return hashlib.sha256(data.encode()).hexdigest()

class Block:
    def __init__(self, index, timestamp, previous_hash, transactions):
        self.index = index
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.merkle_root = self.calculate_merkle_root()
        self.hash = self.calculate_hash()

    def calculate_merkle_root(self):
        transaction_hashes = [tx.hash for tx in self.transactions]
        if len(transaction_hashes) == 0:
            return ""
        elif len(transaction_hashes) == 1:
            return transaction_hashes[0]
        while len(transaction_hashes) > 1:
            next_level = []
            for i in range(0, len(transaction_hashes), 2):
                if i + 1 < len(transaction_hashes):
                    combined = transaction_hashes[i] + transaction_hashes[i + 1]
                    next_level.append(hashlib.sha256(combined.encode()).hexdigest())
                else:
                    next_level.append(transaction_hashes[i])
            transaction_hashes = next_level
        return transaction_hashes[0]

    def calculate_hash(self):
        data = (
            str(self.index)
            + str(self.timestamp)
            + str(self.previous_hash)
            + str(self.merkle_root)
        )
        return hashlib.sha256(data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "0", [])

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        self.chain.append(new_block)

if __name__ == "__main__":
    blockchain = Blockchain()

    tx1 = Transaction("Alice", "Bob", 10)
    tx2 = Transaction("Bob", "Charlie", 5)
    transactions = [tx1, tx2]

    block1 = Block(1, time.time(), blockchain.get_latest_block().hash, transactions)
    blockchain.add_block(block1)

    print("Blockchain:")
    for block in blockchain.chain:
        print(f"Block #{block.index}")
        print(f"Timestamp: {block.timestamp}")
        print(f"Previous Hash: {block.previous_hash}")
        print(f"Merkle Root: {block.merkle_root}")
        print(f"Hash: {block.hash}")
        print("Transactions:")
        for tx in block.transactions:
            print(f"Sender: {tx.sender}, Recipient: {tx.recipient}, Amount: {tx.amount}")
        print()
