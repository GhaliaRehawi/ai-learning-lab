from pathlib import Path
from typing import Tuple, Union

import pandas as pd
import numpy as np


def load_golub(path: Union[str, Path, None] = None) -> Tuple[np.ndarray, pd.Series]:
    """
     Load the Golub leukemia dataset.

     Returns
     X : np.ndarray of shape (n_samples, n_features)
     y : pd.Series of length n_samples
     """

    if path is None:
        # adjust this to match your repo layout
        path = Path(__file__).resolve().parents[1] / "data" / "leukemia_big.csv"
    else:
        path = Path(path)

    df = pd.read_csv(path,header=None)
    # Transpose the df for sklearn functions
    df = df.T
    # Create labels and features
    y = df.iloc[:, 0].astype("category")
    X = df.iloc[:, 1:].astype("float64").to_numpy()

    # Assert that the number of samples in X and y are the same
    assert X.shape[0] == y.shape[0], "Number of samples in X does not match number of samples in y."
    # Assert labels of y
    assert set(y.unique()) == {"ALL", "AML"}, "Unknown label exist."
    # Assert no NaNs in the feature matrix (no missing gene expression values)
    assert not np.isnan(X).any(), "Array contains NaN values."
    # Assert exact number of samples and features
    assert X.shape[0] == 72, f"Expected 72 samples, got {X.shape[0]}"
    assert X.shape[1] == 7128, f"Expected 7128 features, got {X.shape[1]}"

    return X, y