from bucket import PartitionHashTable
import math
import random
import timeit
import pandas as pd

pht = None
n = 1 << 14 # 2^14 = 16384
w = 64
k = 0
c = 5
runs = 1


def init(n, w):
    global pht
    global k
    pht = PartitionHashTable(n, w)
    log_n = int(math.log2(n))
    k = int(log_n**3 + c * log_n**2)

def uniform_benchmark() -> float:
    if pht is None:
        init(n, w)
    
    key_list = random.sample(range(1, n), 40)
    return timeit.timeit(lambda: batch_insert(pht, key_list), number = runs)

def malicious_benchmark() -> float:
    if pht is None:
        init(n, w)
    
    # key_list = random.sample(range(1, n+1), k)
    return timeit.timeit(lambda: malicious_insert(pht), number = runs)

def malicious_insert(pht):
    for i in range(40):
        num_buckets = pht.num_buckets
        m = pht.buckets[0].M
        pht.insert(i*m*num_buckets)


def batch_insert(pht, key_list):
    for key in key_list:
        if not pht.insert(key):
            print("Error: ", key)
            break

def output_data():
    results = []
    data = pd.DataFrame(data = [], columns = ["malicious", "uniform"])
    for i in range(18, 25):
        n = 1 << i
        init(n, w)
        malicious_time = malicious_benchmark()
        uniform_time = uniform_benchmark()
        results.append({
            "n": "1 << {}".format(i),
            "w": w,
            "malicious": malicious_time,
            "uniform": uniform_time,
            "ratio": malicious_time / uniform_time
        })
    data = pd.DataFrame(results)
    data.to_csv("./data.csv")

output_data()