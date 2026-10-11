# Research Methodology & Experimental Design

## 1. Research Questions
1. **RQ1**: Can network telemetry (ICMP ping, SNMP availability, and interface counters) predict future network fault events 30 minutes in advance without data leakage?
2. **RQ2**: Which telemetry feature group provides the highest marginal gain in predictive precision and recall under extreme class imbalance (~5% positive rate)?
3. **RQ3**: How does chronological embargo splitting affect generalization performance compared to unconstrained random splitting?
4. **RQ4**: How can an explainable AI framework bridge the domain shift between emulated ISP topologies and consumer edge Wi-Fi connections?

## 2. Experimental Design
- **Benchmark Corpus**: LCORE-D v2 (22,381 model-ready samples across R1-R7 routers).
- **Split Scheme**: 70% Train, 15% Validation, 15% Test chronologically ordered with a 30-minute embargo buffer.
- **Evaluated Architectures**:
  - Linear Baseline: Logistic Regression (balanced class weights)
  - Bagging Ensemble: Random Forest
  - Boosting Ensembles: HistGradientBoosting, XGBoost, LightGBM
- **Evaluation Metrics**: PR-AUC, ROC-AUC, Precision, Recall, $F_1$, $F_2$, Specificity, False Positive Rate (FPR), False Negative Rate (FNR).
- **Ablation Studies**: Systematic isolation of feature groups:
  1. ICMP-only features
  2. ICMP + SNMP
  3. ICMP + SNMP + Interface metrics
  4. All network telemetry features
  5. All telemetry + router topology
