# Problem Statement — Forecasting Prosumer Energy Behaviour

> One-page brief. Written *before* touching the data, and revisited at the end of the project.

## 1. Context

Enefit (an Estonian energy company) has a fast-growing base of **prosumers**: customers who both **consume** electricity and **produce** it, mostly from rooftop solar panels.

Every hour the company has to balance what its customers use and produce against what it has bought or sold on the market. **When the forecast is wrong, the company pays.** It buys missing energy at short notice or dumps surplus at a poor price. This is called the **imbalance cost**.

As more rooftop solar is installed, prosumer volumes get larger and more weather-dependent, so forecast errors become more expensive.

> **Why this matters beyond Estonia:** Australia has one of the highest rates of rooftop solar in the world. Retailers and the market operator here face the same problem: hard-to-predict solar from rooftop panels.

## 2. Stakeholder

**Energy Trading / Balancing team** at the retailer. They decide how much energy to buy or sell on the day-ahead market and need a reliable hourly forecast to do it.

## 3. Business Question

> **How accurately can we forecast hourly prosumer production and consumption, and how much imbalance cost would a better forecast save compared with the current naive approach?**

Sub-questions for analysis (EDA):
1. How strongly does solar **production** depend on installed capacity, solar radiation and cloud cover?
2. Which customer segments (county, business or household, contract type) contribute most to volume and to forecast error?
3. What daily, weekly and seasonal patterns drive **consumption**?
4. When are forecast errors most expensive, given that electricity prices change hour by hour?

## 4. Decision Supported

Hourly buy/sell volumes on the day-ahead market. A better forecast means smaller positions to correct later at a worse price.

## 5. Scope

| Phase | Target | Why first |
|---|---|---|
| **Phase 1** | Solar **production** | Clear physical link to weather, so easier to explain |
| **Phase 2** | **Consumption** | Driven more by behaviour and calendar effects |

Out of scope: exact replication of the Kaggle leaderboard set-up, real-time deployment.

## 6. Success Metrics

| Type | Metric | Benchmark |
|---|---|---|
| Technical | MAE (kWh), overall and by segment | Naive baselines: same hour 2 days ago, and same hour 7 days ago |
| Business | Estimated imbalance cost (€) | Cost of the naive baseline |

**Imbalance cost proxy (assumption):** the dataset has no real imbalance prices. We estimate cost as
`|forecast error (MWh)| × day-ahead price (€/MWh) × penalty factor`.
This is a stated assumption. The results show the *relative* saving, not an exact euro figure.

## 7. Data & Constraints

- Kaggle competition data: hourly targets, client info (installed capacity), historical and forecast weather, electricity and gas prices.
- **Data-availability timing is critical.** Not all data is known at forecast time (for example, client data and actual targets arrive with a delay). The `data_block_id` column tells us what was available when. Features must respect this, or the model **leaks future information** and looks better than it really is.
- Validation is **time-based** (train on the past, test on the future), never a random split.

## 8. Deliverables

1. Reproducible GitHub repository (SQL + Python)
2. EDA with insights written for a non-technical reader
3. Forecast model vs baselines, with business-cost comparison
4. Dashboard for the trading team
5. Executive summary + LinkedIn article

## 9. Plan (indicative)

| Week | Milestone |
|---|---|
| 1 | Data loaded into DuckDB, data-quality checks, availability-timing understood |
| 2 | EDA + first insights (production) |
| 3 | Baselines + first model (production), time-based validation |
| 4 | Business cost translation, error analysis by segment |
| 5 | Phase 2 (consumption), dashboard |
| 6 | Write-up: README, executive summary, LinkedIn article |

## 10. Risks

| Risk | Mitigation |
|---|---|
| Data leakage via time joins | Join on `data_block_id`; document every feature's availability |
| Large weather tables / joins | Use DuckDB + SQL for heavy joins, pandas only on aggregated data |
| Scope creep | Phase 1 must be finished and written up before Phase 2 |
| Weather → county mapping is approximate | Aggregate weather by county; note the limitation |
