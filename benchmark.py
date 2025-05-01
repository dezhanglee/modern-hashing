from bucket import PartitionHashTable
import math
import random
import timer

pht = None
n = 1 << 14 # 2^14 = 16384
w = 14
k = 0
c = 5

def init(n, w):
    global pht
    global k
    pht = PartitionHashTable(n, w)
    log_n = int(math.log2(n))
    k = int(log_n**3 + c * log_n**2)

def uniform_benchmark():
    if pht is None:
        init(n, w)
    
    key_list = random.sample(range(1, n), 50)
    batch_insert(pht, key_list)

def malicious_benchmark():
    if pht is None:
        init(n, w)
    
    # key_list = random.sample(range(1, n+1), k)
    malicious_insert(pht)

@timer.measure_time
def malicious_insert(pht):
    for i in range(50):
        num_buckets = pht.num_buckets
        m = pht.buckets[0].M
        pht.insert(i*m*num_buckets)


@timer.measure_time
def batch_insert(pht, key_list):
    for key in key_list:
        if not pht.insert(key):
            print("Error: ", key)
            break

malicious_benchmark()
uniform_benchmark()