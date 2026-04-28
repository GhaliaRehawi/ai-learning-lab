import csv
import sys
from collections import defaultdict

def load_and_pivot(path: str) -> dict[str, dict[str, float]]:
    res = defaultdict(dict)
    with open(path ,'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sample = row['sample_id']
            gene = row['gene']
            res[sample][gene] = float(row['expression'])
    return dict(res)



if __name__ == "__main__":
    path = sys.argv[1]
    samples = load_and_pivot(path)
    print(samples)