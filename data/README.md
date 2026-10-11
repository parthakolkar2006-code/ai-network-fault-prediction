# LCORE-D Network-Level Future Fault 30-Minute Dataset

## Purpose
Model-ready network-level dataset created from LCORE-D v2 (R1-R7) for **future network fault prediction within the next 30 minutes**.

## Ground truth
The authoritative target is generated from `Fault Log/FAULT_LOG.csv`, using the 69 logged fault events. The CSV `class` field from the router files is **not used as the target** because its values are not consistent across routers.

## Target definition
`future_fault_30m = 1` when:
- the current timestamp is not inside a logged fault interval;
- the next 30 one-minute timestamps are continuously present;
- at least one logged fault starts after the current timestamp and within the next 30 minutes.

Rows inside current fault intervals are excluded. Censored/gapped 30-minute windows are excluded.

## Dataset statistics
- Common timestamps across R1-R7: 24,167
- Model-ready rows: 22,381
- Positive rows: 1,111
- Negative rows: 21,270
- Positive rate: 4.964%
- Independent logged fault events: 69
- Time range in model-ready data: 2025-10-12 10:50:00 to 2025-11-28 13:42:00
- Features excluding timestamp and target: 79

## Feature groups
- Network-level ICMP loss, ping success, and response-time aggregates
- SNMP availability
- Uptime and path availability
- Topology aggregates (hops/dependents)
- Interface bits received/sent
- Interface packet errors/discards
- Interface-down counts and speed
- Router-specific key telemetry for R1-R7

## Leakage precautions
- No future telemetry is used as an input feature.
- Fault Log is used only to create the future target and current-fault exclusion.
- `class` is intentionally excluded from model features.
- Gateway/IP-like identifiers are not model features.
- Do not randomly split rows for final evaluation; use chronological/event-aware train/validation/test splits with an embargo around boundaries.

## Important research limitation
LCORE-D is an emulated core ISP network dataset. It is suitable for the research/benchmark model, but it is **not consumer-laptop Wi-Fi data**. The final laptop application must be validated separately using real telemetry collected across multiple Wi-Fi networks.
