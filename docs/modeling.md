# Machine Learning Modeling & Threshold Optimization

## 1. Multi-Architecture Benchmark
The research framework trains and compares 5 ML architectures:
1. **Logistic Regression** (L2 penalty, balanced class weighting, StandardScaler)
2. **Random Forest Classifier** (100 estimators, max_depth=12, balanced_subsample)
3. **HistGradientBoostingClassifier** (max_iter=100, class_weight='balanced')
4. **XGBoost Classifier** (scale_pos_weight tuned to positive ratio, max_depth=6)
5. **LightGBM Classifier** (class_weight='balanced', max_depth=6)

## 2. Temporal Splitting with Embargo
Chronological splitting (70% Train, 15% Validation, 15% Test) with a 30-minute embargo buffer:
- **Train partition**: earlier period ($t < t_{\text{train\_end}} - 30\text{m}$)
- **Validation partition**: middle period ($t_{\text{train\_end}} \le t < t_{\text{val\_end}} - 30\text{m}$)
- **Test partition**: latest period ($t \ge t_{\text{val\_end}}$)

## 3. Validation Threshold Optimization
Due to the ~5% rare-event class balance, standard default threshold ($p = 0.5$) is sub-optimal.
- The threshold $\tau \in [0.01, 0.99]$ is swept on the Validation partition to maximize $F_1$ and $F_2$ scores.
- The chosen optimal threshold is locked prior to final evaluation on the held-out Test set.

## 4. Explainable AI (XAI)
- Local attribution maps feature deviations to risk score shifts.
- Explanations isolate the primary contributing signals: ICMP latency spikes, packet loss surges, interface discard events, and SNMP availability degradations.
