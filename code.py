import random
import math
from collections import defaultdict

class Bucket:
    def __init__(self, max_slots, log_n):
        self.slots = [None] * max_slots
        self.count = 0
        self.fingerprints = dict()  # {fingerprint: position}
        self.M = (log_n)**9  # Fingerprint range from Lemma 4.1
        self.seed = random.randint(1, 1000000)  # Per-bucket seed
        
    def fingerprint(self, key):
        # Simple fingerprint using seed and modular hashing
        return (self.seed * key) % self.M
    
    def insert(self, key):
        f = self.fingerprint(key)
        if f in self.fingerprints:
            # Collision: Rebuild the bucket
            self.rebuild()
            return self.insert(key)  # Retry insertion
        
        pos = self.count
        self.slots[pos] = key
        self.fingerprints[f] = pos
        self.count += 1
        return True
    
    def rebuild(self):
        # Generate new seed and rehash all keys
        self.seed = random.randint(1, 1000000)
        new_fingerprints = {}
        for i in range(self.count):
            key = self.slots[i]
            f = self.fingerprint(key)
            if f in new_fingerprints:
                # Rebuild failed, try again
                self.rebuild()
                return
            new_fingerprints[f] = i
        self.fingerprints = new_fingerprints
    
    def query(self, key):
        f = self.fingerprint(key)
        if f not in self.fingerprints:
            return False
        pos = self.fingerprints[f]
        return self.slots[pos] == key
    
    def delete(self, key):
        if not self.query(key):
            return False
        f = self.fingerprint(key)
        pos = self.fingerprints[f]
        # Move last element to this position
        last_pos = self.count - 1
        self.slots[pos], self.slots[last_pos] = self.slots[last_pos], self.slots[pos]
        # Update fingerprint for moved key
        moved_key = self.slots[pos]
        moved_f = self.fingerprint(moved_key)
        del self.fingerprints[f]
        self.fingerprints[moved_f] = pos
        # Remove last element
        self.slots[last_pos] = None
        self.count -= 1
        return True

class PartitionHashTable:
    def __init__(self, n, w):
        self.n = n
        self.w = w
        log_n = math.log2(n)
        self.bucket_size = int(log_n**3 + 100 * log_n**2)  # Example parameters
        self.num_buckets = n // self.bucket_size
        self.buckets = [Bucket(self.bucket_size, log_n) for _ in range(self.num_buckets)]
        self.hash_to_bucket = lambda key: key % self.num_buckets  # Simple hash
    
    def insert(self, key):
        bucket_idx = self.hash_to_bucket(key)
        return self.buckets[bucket_idx].insert(key)
    
    def query(self, key):
        bucket_idx = self.hash_to_bucket(key)
        return self.buckets[bucket_idx].query(key)
    
    def delete(self, key):
        bucket_idx = self.hash_to_bucket(key)
        return self.buckets[bucket_idx].delete(key)

class KtrieNode:
    def __init__(self):
        self.children = defaultdict(KtrieNode)
        self.value = None  # For existence marker

class Ktrie:
    def __init__(self, k):
        self.k = k
        self.log_k = int(math.log2(k))
        self.root = KtrieNode()
    
    def _split_key(self, key):
        chunks = []
        mask = (1 << self.log_k) - 1
        while key > 0:
            chunks.append(key & mask)
            key >>= self.log_k
        return chunks[::-1]  # Process MSB first
    
    def insert(self, key):
        node = self.root
        for chunk in self._split_key(key):
            node = node.children[chunk]
        node.value = True
    
    def contains(self, key):
        node = self.root
        for chunk in self._split_key(key):
            if chunk not in node.children:
                return False
            node = node.children[chunk]
        return node.value is not None

class DeamortizedHashTable(PartitionHashTable):
    def __init__(self, n, w):
        super().__init__(n, w)
        self.growing_trie = Ktrie(int(math.sqrt(n)))
        self.shrinking_trie = Ktrie(int(math.sqrt(n)))
        self.operations_since_swap = 0
        self.batch_size = int(n**0.25)
    
    def process_batch(self):
        # Process some operations from shrinking trie
        # (This would involve iterating over trie entries and applying to main table)
        pass
    
    def insert(self, key):
        self.growing_trie.insert(key)
        self.operations_since_swap += 1
        if self.operations_since_swap >= self.batch_size:
            # Swap tries and process
            self.growing_trie, self.shrinking_trie = self.shrinking_trie, self.growing_trie
            self.operations_since_swap = 0
            self.process_batch()  # Process all in shrinking trie
    
    def delete(self, key):
        # Similar to insert, but with deletion logic
        pass  # Needs trie deletion implementation
