# ai-learning-lab

### 8-Week ML and AI bootcamp for computational biologists with Perplexity Computer agents

Goal: build durable coding fluency, software engineering habits, and ML foundations, anchored in computational biology projects.

- Week 1 — Python fluency + Git hygiene 

    - PIdiomatic ython (comprehensions, iterators, generators, dataclasses, typing)

    - Virtual envs, dependency pinning, project layout

    - Git: branches, rebase vs merge, atomic commits, PR workflow

    - Mini-project: refactor a messy bioinformatics script into a clean package

- Week 2 — Testing, debugging, defensive code

  - pytest, fixtures, parametrize, coverage

  - pdb, logging vs print, assertions, contracts

  - Common bugs: off-by-one, mutable defaults, broadcasting traps

  - Mini-project: add tests + CI to Week 1 package

- Week 3 — ML foundations I (supervised learning)

  - Bias-variance, train/val/test discipline, data leakage

  - Linear/logistic regression from scratch, regularization

  - Metrics: ROC-AUC, PR-AUC, calibration, class imbalance

  - Mini-project: predict a binary phenotype from tabular omics features

- Week 4 — ML foundations II (trees, ensembles, validation)

  - Decision trees, random forests, gradient boosting (intuition + math)

  - Cross-validation strategies for biological data (group, stratified, leave-one-subject-out)

  - Feature importance, SHAP, pitfalls

  - Mini-project: benchmark logistic vs XGBoost on the Week 3 dataset, with leakage-safe CV

- Week 5 — Deep learning core

  - Backprop, optimizers, init, normalization, regularization

  - PyTorch idioms: Datasets/DataLoaders, training loops, mixed precision

  - Reproducibility: seeds, determinism, config management

  - Mini-project: MLP + 1D CNN on a sequence classification task

- Week 6 — Representation learning + Transformers

  - Embeddings, contrastive learning, attention, positional encodings

  - Transformer block from scratch, then HuggingFace usage

  - Tokenization for biology (k-mers, BPE, residue-level)

  - Mini-project: fine-tune a small protein language model on a downstream task

- Week 7 — Graph ML for biology

  - GNN intuition: message passing, GCN, GAT, GraphSAGE

  - PyG basics, batching graphs, over-smoothing

  - Application: gene regulatory network or PPI node classification

  - Mini-project: GNN on a small biological graph with proper splits

- Week 8 — Capstone + engineering polish

  - Pick one: GRN inference, variant effect prediction, or cell-cell communication

  - End-to-end: data → model → evaluation → ablations → write-up

  - Engineering: config files, experiment tracking, README, reproducibility

Deliverable: portfolio-ready GitHub repo + short technical report

Each week ends with: recall questions, weak-area review, and a written reflection.