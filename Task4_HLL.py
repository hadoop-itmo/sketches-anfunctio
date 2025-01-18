import mmh3
import math
from utils import gen_grouped_seq


class HyperLogLog:
    def __init__(self, p=14):
        self.p = p
        self.m = 1 << p
        self.M = [0] * self.m

    def _hash(self, x):
        return mmh3.hash(x)

    def add(self, x):
        hash_value = self._hash(x)
        j = hash_value & (self.m - 1)
        w = hash_value >> self.p
        rho = self._rho(w)
        self.M[j] = max(self.M[j], rho)

    def _rho(self, w):
        if w == 0:
            return 64
        return len(bin(w)[2:].rstrip('0')) - 1 if bin(w)[2:].rstrip('0') else 64

    def estimate(self):
        E = self.m * self._alpha(self.m) / sum([2**(-M) for M in self.M])
        V = sum([1 for M in self.M if M == 0])
        if V != 0:
            return self.m * math.log(self.m / V)
        elif E <= (5 * self.m / 2):
            return E
        else:
            return -(self.m * math.log(1 - (E / self.m)))

    def _alpha(self, m):
        if m == 16:
            return 0.673
        elif m == 32:
            return 0.697
        elif m == 64:
            return 0.709
        else:
            return 0.7213 / (1 + 1.079 / m)


if __name__ == '__main__':
  # данные для эксперимента
  patterns = [[(100, 1), (2, 400)], [(15, 10)], [(1000, 1)]]
  p_values = [12, 14, 16]
  
  for pattern in patterns:
      for p in p_values:
          name = f'data_hll_{pattern}.txt'
          gen_grouped_seq(name, pattern)
          
          with open(name, 'rt') as file:
              data = [line.strip().split(',')[0] for line in file]
          
          hll = HyperLogLog(p)
          for key in data:
              hll.add(key)
          
          estimated_unique = hll.estimate()
          actual_unique = len(set(data))
          
          print(f'Паттерн: {pattern}, p: {p}')
          print(f'Оценка уникальных объектов: {estimated_unique}, действительное количество уникальных объектов: {actual_unique}')
          print(f'Ошибка оценки: {(estimated_unique - actual_unique) / actual_unique * 100 if actual_unique != 0 else 0}%')
          print()
