import numpy as np
import pandas as pd
import mmh3
from utils import gen_uniq_seq


class CountingBloomFilter:
    def __init__(self, n, k, cap): 
        self.n = n
        self.k = k
        self.cap = cap
        self.bits_array = 64 // cap
        self.array_size = (self.n + self.bits_array - 1) // self.bits_array
        self.array = np.zeros(self.array_size, dtype=np.uint64)

    def _hash(self, s, seed):
        hash_value = mmh3.hash(s, seed) % self.n
        return hash_value

    def put(self, s):
        for i in range(self.k): # k - number of hashes
            index = self._hash(s, i)
            counter_index = index // self.bits_array
            bit_position = (index % self.bits_array) * self.cap
            
            current_value = (self.array[counter_index] >> np.uint64(bit_position)) & np.uint64(((1 << self.cap) - 1))
            if current_value < np.uint64((1 << self.cap) - 1):  # max size checking
                current_value += 1
                self.array[counter_index] |= (np.uint64(current_value) << np.uint64(bit_position))


    def get(self, s):
        for i in range(self.k):  # k - number of hashes
            index = self._hash(s, i)
            counter_index = index // self.bits_array
            bit_position = (index % self.bits_array) * self.cap

            if ((self.array[counter_index] >> np.uint64(bit_position)) & np.uint64(((1 << self.cap) - 1))) == 0:
                return False
        return True

    def size(self):
        return sum(bin(counter).count('1') for counter in self.array) / self.k
    

def run_experiments_3(experiments):
    results = []
    for experiment in experiments:
        cbf = CountingBloomFilter(n = experiment['bf_size'],
                                  k = experiment['k'],
                                  cap = experiment['cap'])
        
        gen_uniq_seq('counting_test', experiment['set_size'])

        fp_count = 0
        with open('counting_test') as file:
            for line in file:
                if cbf.get(line):
                    fp_count += 1
                cbf.put(line)
            ones_count = cbf.size()
        
        results.append({"k": experiment["k"],
                        "bf_size": experiment["bf_size"],
                        "set_size": experiment["set_size"],
                        "cap": experiment["cap"],
                        "fp_count": fp_count,
                        "ones_count": ones_count})

    return results


if __name__ == '__main__':
    set_size = 1000000
    bf_size = 10000
    k_opt = int(set_size / bf_size * np.log(2))

    experiments = [{"k": 3, "bf_size": 100, "set_size": 10000, "cap": 4},
                   {"k": 5, "bf_size": 1000, "set_size": 10000, "cap": 8},
                   {"k": 7, "bf_size": 10000, "set_size": 10000, "cap": 16},
                   {"k": 5, "bf_size": 1000, "set_size": 10000, "cap": 8},
                   {"k": k_opt, "bf_size": bf_size, "set_size": set_size, "cap": 1},
                   {"k": k_opt, "bf_size": bf_size, "set_size": set_size, "cap": 8},
                   {"k": k_opt, "bf_size": bf_size, "set_size": set_size, "cap": 16}]

    results = run_experiments_3(experiments)

    res3 = pd.DataFrame(results)
    print(res3)
