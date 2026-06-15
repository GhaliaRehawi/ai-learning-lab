from pathlib import Path
import numpy as np

from disease_classifier.data import load_golub
from utils.utils import read_config_file
from disease_classifier.train import run_cv

from sklearn.linear_model import LogisticRegression



def main() -> None:
    X, y = load_golub()
    y_num = y.map({"ALL": 0, "AML": 1}).astype(int)
    # 1) Set Up The Experiment

    # Set up working path
    path = Path(__file__).resolve().parents[1]
    # Read config file
    config = read_config_file(str(path) + '/configs/golub_logreg.yml')

    data_path = config['data']['path']
    model_name = config['model']['type']

    # Initialize the model
    if model_name == "logistic_regression":
        clf = LogisticRegression(max_iter=1000, class_weight=config['model']['class_weight'])
    else:
        raise ValueError(f"Model {model_name} not supported.")

    # Run cv and print evaluation results across folds
    cv_results = run_cv(X, y_num, clf, config['cv']['n_splits'], config['cv']['random_state'])

    print("ROC-AUC scores:", cv_results["test_roc_auc"])
    print("PR-AUC scores:", cv_results["test_pr_auc"])
    print(f"Mean ROC-AUC: {np.mean(cv_results['test_roc_auc']):.3f} ± {np.std(cv_results['test_roc_auc']):.3f}")
    print(f"Mean PR-AUC:  {np.mean(cv_results['test_pr_auc']):.3f} ± {np.std(cv_results['test_pr_auc']):.3f}")

    # In case of high Precision (TP/TP+FP) and low Recall (TP/TP+FN), we can say that the model is good
    # at identifying positive cases (AML) but misses many of them, leading to a high number of
    # false negatives (AML cases classified as ALL). This could be problematic in a medical context
    # where missing a diagnosis can have serious consequences.
    # We might want to adjust the model or threshold to improve recall, even if it means sacrificing some precision.
    # We can do this by penalizing the model more when it predicts the positve class wrongly
    # clf = LogisticRegression(max_iter=1000, class_weight="balanced")



if __name__ == "__main__":
    main()