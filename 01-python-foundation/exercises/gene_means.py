import csv
import sys
from collections import defaultdict
from statistics import mean

def gene_means(path: str) -> dict[str, float]:
    """compute per-gene mean expression across samples"""
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        data = defaultdict(list) # auto-initializes any new key to []
        for row in reader:
            data[row["gene"]].append(float(row["expression"])) # shape {gene1: [exp1,exp2,,]}

    return {gene: mean(values) for gene, values in data.items()}


if __name__ == "__main__":
    expr_mean = gene_means(sys.argv[1])
    print(expr_mean)