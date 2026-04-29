import csv
import sys
from collections import defaultdict
from statistics import mean

def gene_means(path: str) -> dict[str, float]:
    """compute per-gene mean expression across samples"""
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        data = defaultdict(list)
        for row in reader:
            data[row["gene"]].append(float(row["expression"]))

    return {gene: mean(values) for gene, values in data.items()}


if __name__ == "__main__":
    # todo: add file expression.csv to data/
    expr_mean = gene_means(sys.argv[1])
    print(expr_mean)