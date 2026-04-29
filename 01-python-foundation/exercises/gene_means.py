import csv
import sys
from collections import defaultdict
from statistics import mean

def calculate_gene_expression_mean(path:str) -> dict[str, float]:
    """compute per-gene mean expression across samples"""
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        data = defaultdict(list)
        for row in reader:
            data[row["gene"]].append(float(row["expression"]))

    means = {}
    for gene, expr_list in data.items():
        means[gene] = mean(expr_list)
    return dict(means)


if __name__ == "__main__":
    # todo: add file expression.csv to data/
    expr_mean = calculate_gene_expression_mean(sys.argv[1])
    print(expr_mean)