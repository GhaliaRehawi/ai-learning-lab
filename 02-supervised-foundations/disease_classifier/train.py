import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_validate
from sklearn.linear_model import LogisticRegression


def run_cv(X: np.ndarray, y: pd.Series, cv_splits:int, random_state:int, model_name ="logistic_regression") -> np.ndarray:
    """
     Carry out k-fold cross validation on the given model and dataset.

     Returns
     cv_results: np.ndarray of shape (cv_splits,) containing the ROC-AUC and PR-AUC scores for each fold
     """

    cv = StratifiedKFold(n_splits=cv_splits, random_state=random_state, shuffle=True)

    # We can extend this to carry out hyperpameter tuning e.g. different values for class_weights etc.
    if model_name == "logistic_regression":
        clf = LogisticRegression(max_iter=1000, class_weight="balanced")
    else:
        raise ValueError(f"Model {model_name} not supported.")


    scoring = {
        "roc_auc": "roc_auc",
        "pr_auc": "average_precision",
    }

    cv_results = cross_validate(
        clf,
        X,
        y,
        cv=cv,
        scoring=scoring,
        return_train_score=False,
    )

    return cv_results