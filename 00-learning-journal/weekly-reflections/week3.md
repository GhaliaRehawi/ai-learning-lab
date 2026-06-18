# Week 3 — Reflection 
In Week 3 you built your first end‑to‑end supervised learning pipeline on a real gene expression dataset (Golub leukemia), focusing on logistic regression, proper data shaping, and evaluation metrics beyond accuracy.

You worked with the Golub leukemia dataset (“leukemia_big.csv”), where:

- Rows correspond to genes (~7,128 features per sample).

- Columns correspond to patient samples (72 samples).

- Labels (ALL vs AML) are provided in the file and needed to be extracted and aligned correctly with the feature matrix.

## Data loading and preprocessing
You implemented a load_golub() function that:

- Loads the CSV into a pandas DataFrame.

- Transposes it so the shape matches sklearn’s convention: X has shape(n_samples , n_features)= (72, 7128). y has shape(n_samples,)
with labels "ALL" and "AML".

- Extracts labels and features correctly after transposition:

- Includes invariants / assertions to catch silent bugs: Sample counts in X and y match, lbels are exactly {"ALL", "AML"}. and no NaNs in the feature matrix (or at least detected explicitly).


## Supervised learning and logistic regression
You then built a baseline binary classifier using logistic regression:

Logistic regression models the log-odds of the positive class as a linear function of the features:

logit(P(AML ∣ x))= w^T x+ b

After fitting the parameters (w , b), the model outputs:

A probability p= P(AML ∣ x) via the sigmoid function.

A class prediction (AML vs ALL) by applying a threshold, usually 
p ≥ 0.5

You used sklearn’s LogisticRegression.

## Class imbalance and evaluation metrics
You spent time on why accuracy alone is misleading, especially for medical/imbalanced problems:

With many more ALL than AML cases, a model could be “accurate” while missing most AML patients.

Instead of relying on a single accuracy number, you focused on:

Confusion matrix:

- True positives (TP): AML correctly predicted.

- False positives (FP): ALL predicted as AML.

- True negatives (TN): ALL correctly predicted.

- False negatives (FN): AML predicted as ALL.

Precision and recall:

- Precision (for AML) = TP / (TP + FP):
“Of all predicted AML, how many are truly AML?”

- Recall / sensitivity (for AML) = TP / (TP + FN):
“Of all true AML patients, how many did we catch?”

In medical settings you emphasized:

- Reducing false negatives (higher recall) is often crucial.

- Higher recall usually comes at the cost of lower precision.

ROC and ROC‑AUC:

- ROC curve plots TPR vs FPR as you vary the decision threshold.

- ROC‑AUC summarizes how well the model ranks AML vs ALL across all thresholds.

Precision–Recall (PR) curve and PR‑AUC:

- PR curve plots precision vs recall for the positive class (AML) over thresholds.

- PR‑AUC is especially informative for imbalanced datasets, focusing on performance on the minority (disease) class.

You also clarified how changing the probability threshold affects behavior:

Lowering the threshold for AML (e.g. from 0.5 to 0.2):

- Increases recall (fewer AML patients missed).

- Often reduces precision (more ALL patients incorrectly flagged as AML).

A strong model maintains relatively high precision even at higher recall.

## Cross‑validation, model selection, and final model
You implemented stratified k‑fold cross‑validation to get more reliable performance estimates:

StratifiedKFold: ensures each fold has similar AML/ALL proportions.

cross_validate with multiple scoring metrics:

- "roc_auc" for ROC‑AUC.

- "average_precision" for PR‑AUC (area under the precision–recall curve).

## Code organization and config-driven design
You organized your code into functions and modules for clarity and reusability.

A simple YAML config file (config.yml) describing:

Model type and hyperparameters (type, C, class_weight, max_iter).

CV settings (n_splits, random_state).

Optional data path override.

A small loader that reads the config and builds the model accordingly.

You then used CV to:

Compare different hyperparameter settings (e.g. different C, with/without balancing).

Select the best configuration based on mean PR‑AUC (and ROC‑AUC as supporting evidence).

You also discussed the standard practice after CV:

Model selection: use CV results only on a train/validation split to choose model type and hyperparameters.

Final training: retrain a fresh model with those chosen settings on all non‑test data.

Final evaluation: evaluate once on the held‑out test set, which was never touched during tuning, to get an unbiased estimate of generalization.

You explicitly connected this to avoiding information leakage: the test set should not influence hyperparameter tuning or model selection decisions.