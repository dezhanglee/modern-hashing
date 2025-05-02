# bucket 
import random
import math

class Bucket:
    def __init__(self, log_n, max_slots):
        self.max_slots = max_slots  # e.g., log³n + O(log²n)
        self.slots = [None] * self.max_slots
        self.count = 0
        self.fingerprints = dict()  # {fingerprint: position}
        self.M = int((log_n) ** 9)  # Fingerprint range
        self.seed = random.getrandbits(64)  # 64-bit seed for better randomness
        
    def _compute_fingerprint(self, key):
        # Use a simple seeded hash (multiply and mod)
        return (self.seed * key) % self.M
    
    def insert(self, key):
        f = self._compute_fingerprint(key)
        if f in self.fingerprints:
            # Collision: Rebuild the bucket
            self.rebuild()
            return self.insert(key)  # Retry after rebuild
        
        # Insert into the next available slot
        pos = self.count
        self.slots[pos] = key
        self.fingerprints[f] = pos
        self.count += 1
        return True
    
    def rebuild(self):
        # Generate a new seed and rehash all keys
        new_seed = random.getrandbits(64)
        new_fingerprints = {}
        new_slots = [None] * self.max_slots
        new_count = 0
        
        for key in self.slots[:self.count]:
            f = (new_seed * key) % self.M
            if f in new_fingerprints:
                # Retry with a new seed if collision occurs
                self.rebuild()
                return
            new_fingerprints[f] = new_count
            new_slots[new_count] = key
            new_count += 1
        
        # Update bucket state
        self.seed = new_seed
        self.slots = new_slots
        self.fingerprints = new_fingerprints
        self.count = new_count
    
    def query(self, key):
        f = self._compute_fingerprint(key)
        if f not in self.fingerprints:
            return False
        pos = self.fingerprints[f]
        return self.slots[pos] == key
    
    def delete(self, key):
        if not self.query(key):
            return False
        f = self._compute_fingerprint(key)
        pos = self.fingerprints.pop(f)
        # Move the last element to this position
        last_pos = self.count - 1
        if pos != last_pos:
            self.slots[pos], self.slots[last_pos] = self.slots[last_pos], self.slots[pos]
            # Update the moved key's fingerprint entry
            moved_key = self.slots[pos]
            moved_f = self._compute_fingerprint(moved_key)
            self.fingerprints[moved_f] = pos
        self.slots[last_pos] = None
        self.count -= 1
        return True
    
class PartitionHashTable:
    def __init__(self, n, w):
        self.n = n  # Current number of keys
        self.w = w  # Word size (bits)
        log_n = math.log2(n)
        self.bucket_size = int(log_n**3 + 100 * log_n**2)  # Example bucket size
        self.num_buckets = n // self.bucket_size
        self.buckets = [Bucket(log_n, self.bucket_size) for _ in range(self.num_buckets)]
        
    def hash_to_bucket(self, key):
        return key % self.num_buckets  # Simple modulo hash
    
    def insert(self, key):
        bucket_idx = self.hash_to_bucket(key)
        return self.buckets[bucket_idx].insert(key)
    
    def delete(self, key):
        bucket_idx = self.hash_to_bucket(key)
        return self.buckets[bucket_idx].delete(key)
    
    def query(self, key):
        bucket_idx = self.hash_to_bucket(key)
        return self.buckets[bucket_idx].query(key)