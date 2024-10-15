import numpy as np
import pandas as pd
import mmh3
from utils import gen_uniq_seq


class BloomFilter_k:
    def __init__(self, k, n):
        self.k = k
        self.n = n
        self.array = np.zeros(self.n, dtype = int)

    def _hash(self, string):
        hash_value = [mmh3.hash(string, i) % self.n for i in range(self.k)]
        return hash_value

    def put(self, string):
        for hash_value in self._hash(string):
            self.array[hash_value] = True

    def get(self, string):
        return all(self.array[hash_value] for hash_value in self._hash(string))

    def size(self):
        return np.count_nonzero(self.array) / self.k


def generating_sequences(set_sizes):
    for set_size in set_sizes:
        gen_uniq_seq(str(set_size), set_size)


def run_experiments_2(k, bf_sizes, set_sizes):
    results = []

    for _k in k:
        for set_size in set_sizes:
            for bf_size in bf_sizes:
                bf = BloomFilter_k(k = _k, n = bf_size)
            
                fp_count = 0
                with open(f'{set_size}') as file: 
                    for s in file:
                        if bf.get(s):
                            fp_count += 1
                        bf.put(s)
                    ones_count = bf.size()

                results.append({'k': _k,
                                'bf_size': bf_size, 
                                'set_size': set_size,
                                'fp_count': fp_count,
                                'ones_count': ones_count})
    
    return results


if __name__ == '__main__':
    k = [1, 2, 3, 4]
    bf_sizes = [8, 64, 1024, 64000, 16000000]
    set_sizes = [5, 50, 500, 5000, 5000000]

    results = run_experiments_2(k, bf_sizes, set_sizes)
    res2 = pd.DataFrame(results)
    print(res2)