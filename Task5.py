import csv
from collections import defaultdict
from utils import gen_grouped_seq


KEY_THRESHOLD = 60000


def count_key_occurrences(file_path, key_column=0):
    key_occurrences = defaultdict(int)

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for record in csv_reader:
            key = record[key_column]
            key_occurrences[key] += 1

    return key_occurrences


def find_keys_w_problem(counts_file1, counts_file2):
    problematic_keys = set()

    for key, count in counts_file1.items():
        if count > KEY_THRESHOLD or counts_file2.get(key, 0) > KEY_THRESHOLD:
            problematic_keys.add(key)

    for key, count in counts_file2.items():
        if key not in counts_file1 and count > KEY_THRESHOLD:
            problematic_keys.add(key)

    return problematic_keys


def main(file1_path, file2_path):
    counts_file1 = count_key_occurrences(file1_path)
    counts_file2 = count_key_occurrences(file2_path)
    problem_keys = find_keys_w_problem(counts_file1, counts_file2)

    print(f'Число проблемных ключей = {len(problem_keys)}')


if __name__ == '__main__':
    pattern = [(4, 100000), (7, 65000), (12, 40000), (2, 71000), (3, 50000)]
    gen_grouped_seq('test1.csv', pattern = pattern, n_extra_cols = 0, to_shuffle = True)
    gen_grouped_seq('test2.csv', pattern = pattern, n_extra_cols = 0, to_shuffle = True)

    main('test1.csv', 'test2.csv')