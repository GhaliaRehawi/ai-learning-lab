import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_validate


def run_cv(X: np.ndarray, y: pd.Series, model, cv_splits:int, random_state:int) -> np.ndarray:
    """
     Carry out k-fold cross validation on the given model and dataset.

     Returns
     cv_results: np.ndarray of shape (cv_splits,) containing the ROC-AUC and PR-AUC scores for each fold
     """
    cv = StratifiedKFold(n_splits=cv_splits, random_state=random_state, shuffle=True)

    scoring = {
        "roc_auc": "roc_auc",
        "pr_auc": "average_precision",
    }

    cv_results = cross_validate(
        model,
        X,
        y,
        cv=cv,
        scoring=scoring,
        return_train_score=False,
    )

    return cv_results

#def train():
    #input X training data
    #apply startified kfold cross validation