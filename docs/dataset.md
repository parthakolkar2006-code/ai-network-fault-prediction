# Dataset Documentation: LCORE-D v2

## 1. Overview
- **Dataset**: `lcore_d_network_future_fault_30m.csv`
- **Total Model-Ready Rows**: 22,381
- **Input Features**: 79 (excluding timestamp and target)
- **Positive Samples**: 1,111
- **Negative Samples**: 21,270
- **Base Positive Class Imbalance**: ~4.964%
- **Independent Logged Fault Events**: 69
- **Time Range**: 2025-10-12 10:50:00 to 2025-11-28 13:42:00

## 2. Authoritative Ground Truth Definition
The future fault ground truth is anchored strictly to `fault_log_clean.csv`:
$$\text{future\_fault\_30m} = 1$$
if a logged network fault starts within the upcoming 30 minutes ($t + 1\text{m}$ to $t + 30\text{m}$), provided that the current timestamp $t$ is outside an ongoing fault and the 30-minute observation window has no censorship/gaps.

## 3. Strict Precautions Against Data Leakage
1. **No Target Recreation from `class`**: The CSV `class` column reflects router-local transient states and is excluded from predictive features.
2. **Exclusion of Ongoing Fault Intervals**: Rows occurring during active faults are filtered to evaluate *predictive anticipation*, not trivial detection.
3. **No Future Leakage**: No forward rolling metrics or future-derived aggregates are included in the feature set.
4. **Chronological Embargo Split**: A 30-minute embargo buffer is enforced between train, validation, and test boundaries to ensure overlapping 30m future windows cannot leak labels into subsequent splits.
