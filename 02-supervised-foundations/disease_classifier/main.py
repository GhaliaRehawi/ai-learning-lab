from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from disease_classifier.data import load_golub
from utils.utils import read_config_file
from disease_classifier.train import run_cv

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import RocCurveDisplay, PrecisionRecallDisplay, roc_curve, auc, precision_recall_curve

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

    # Run cv and print evaluation results across folds
    if model_name == "logistic_regression":
        cv_results = run_cv(X, y_num, config['cv']['n_splits'], config['random_state'], model_name)
        # Train the final model
        clf = LogisticRegression(max_iter=1000, class_weight=config['model']['class_weight'])
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=config['random_state'], stratify=y)
        clf.fit(X_train, y_train)
        # Get probabilities for the positive class (AML)
        y_proba = clf.predict_proba(X_test)[:, list(clf.classes_).index("AML")]

        # ROC curve shows the model performance on different thresholds p and reports TPR (recall) and FPR (FP/FP + TN)
        fpr, tpr, roc_thresholds = roc_curve(y_test, y_proba, pos_label="AML")
        roc_auc = auc(fpr, tpr)
        #RocCurveDisplay(fpr=fpr, tpr=tpr).plot()
        #plt.savefig("roc_golub_logreg.png", dpi=150, bbox_inches="tight")
        #plt.close()

        # PR curve shows the model performance on different thresholds p and reports TPR (recall) and precision
        # PR‑AUC is especially informative when positives are rare
        precision, recall, pr_thresholds = precision_recall_curve(y_test, y_proba, pos_label="AML")
        pr_auc = auc(recall, precision)
        #PrecisionRecallDisplay(precision=precision, recall=recall).plot()
        #plt.savefig("PR_golub_logreg.png", dpi=150, bbox_inches="tight")
        #plt.close()
    else:
        raise ValueError(f"Model {model_name} not supported.")

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

    print("ROC-AUC score of the final model:", roc_auc)
    print("PR-AUC score of the final model:", pr_auc)





if __name__ == "__main__":
    main()