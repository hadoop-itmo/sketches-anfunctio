import numpy as np
import mmh3
from bitarray import bitarray
from utils import gen_uniq_seq


class BloomFilter_1:
    def __init__(self, n):
        self.n = n
        self.array = bitarray(n)
        self.array.setall(0)
        self.size_count = 0

    def _hash(self, string):
        hash_value = mmh3.hash(string) % self.n
        return hash_value

    def put(self, string):
        index = self._hash(string)
        if not self.array[index]:
            self.array[index] = 1
            self.size_count += 1

    def get(self, string):
        index = self._hash(string)
        return bool(self.array[index])

    def size(self):
        return self.size_count


if __name__ == '__main__':
    bf_sizes = [8, 64, 1024, 64000, 16000000]
    set_sizes = [5, 50, 500, 5000, 5000000]

    for set_size in set_sizes:
        gen_uniq_seq(f'data_{set_size}.txt', set_size)
    
    results = []
    for set_size in set_sizes:
      for bf_size in bf_sizes:
        fp_count = 0
        bf = BloomFilter_1(bf_size)
        with open(f'data_{set_size}.txt', 'rt') as file:
          for line in file:
            if bf.get(line):
              fp_count += 1
            bf.put(line)
          
          ones_count = bf.size()
          results.append((bf_size, set_size, fp_count, ones_count))

    print()
    print('------------------------------------------')
    print(' bf_size | set_size | fp_count  | ones_count')
    print('------------------------------------------')
    for result in results:
      print(f'{result[0]:<8} | {result[1]:<8} | {result[2]:<9} | {result[3]}')
