import mmh3
import numpy as np
from utils import gen_uniq_seq
from tqdm import tqdm
from bitarray import bitarray


class BloomFilter_k:
    def __init__(self, k, n):
        self.n = n
        self.k = k
        self.array = bitarray(n)
        self.array.setall(0)
        self.size_count = 0

    def _hash(self, string, seed):
        return mmh3.hash(string, seed) % self.n

    def put(self, string):
        for seed in range(self.k):
            index = self._hash(string, seed)
            if not self.array[index]:
                self.array[index] = 1
                self.size_count += 1

    def get(self, string):
        for seed in range(self.k):
            index = self._hash(string, seed)
            if not self.array[index]:
                return False
        return True

    def size(self):
        return self.size_count / self.k


if __name__ == '__main__':
    bf_sizes = [8, 64, 1024, 64000, 16000000]
    set_sizes = [5, 50, 500, 5000, 5000000]
    k = [1, 2, 3, 4]

    for set_size in set_sizes:
        gen_uniq_seq(f'data_{set_size}.txt', set_size)
    
    results = []
    for _k in tqdm(k, desc = 'Изменяем число хэш-функций'):
      for set_size in set_sizes:
        for bf_size in bf_sizes:
          bf = BloomFilter_k(_k, bf_size)
          fp_count = 0
          
          with open(f'data_{set_size}.txt', 'rt') as file:
            for line in file:
              if bf.get(line):
                fp_count += 1
              bf.put(line)
            
            ones_count = bf.size()
            results.append((_k, bf_size, set_size, fp_count, ones_count))

    print()
    print('----------------------------------------------')
    print('k | bf_size | set_size | fp_count | ones_count')
    print('----------------------------------------------')
    for result in results:
      print(f'{result[0]} | {result[1]:<7} | {result[2]:<8} | {result[3]:<9} | {result[4]:.2f}')
