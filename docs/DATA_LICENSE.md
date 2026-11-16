# Data Licence & Compliance

This project uses data from the Kaggle competition
[Enefit – Predict Energy Behavior of Prosumers](https://www.kaggle.com/competitions/predict-energy-behavior-of-prosumers),
provided by **Eesti Energia AS** and hosted by **Kaggle**.

- **Data licence:** [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) (Attribution · Non-Commercial · Share-Alike), subject to the competition rules.
- **This is an independent, non-commercial portfolio project.** It is not affiliated with, endorsed by or sponsored by Eesti Energia AS, Enefit or Kaggle.

## What this repository does and does not contain

| Included ✅ | Not included ❌ |
|---|---|
| Source code (Python, SQL) | Raw competition files (`*.csv`) |
| Documentation and methodology | Processed data (DuckDB database, parquet, extracts) |
| Charts and **aggregated** summary tables | Row-level data, samples or reconstructed tables |
| | Trained model files |

To reproduce the analysis, accept the competition rules on Kaggle and download the data yourself (see the main README).

## Licensing of this repository

| Content | Licence |
|---|---|
| Source code | MIT (see `LICENSE`) |
| Figures, aggregated results and written analysis derived from the data | CC BY-NC-SA 4.0, with attribution to Eesti Energia AS / Kaggle |

## Working rules for this project

1. **Never commit data.** Raw or processed data, row-level samples and model files are git-ignored.
2. **Notebooks are stored as `.py` (percent format) without outputs.** Raw rows printed during exploration are never committed. If `.ipynb` files are used, clear outputs before committing.
3. **Publish aggregates only.** Charts and tables show aggregated values (for example monthly totals or segment averages). They never contain full row-level series that could rebuild the dataset.
4. **Attribute everywhere.** README, dashboard and articles credit *"Data: Eesti Energia AS / Kaggle, CC BY-NC-SA 4.0"*.
5. **Non-commercial only.** No use in paid products or services.
6. **No raw data to third parties.** Raw files stay on the author's machine (or on Kaggle). Only aggregated outputs are shared.
7. **Public dashboards use aggregated extracts only**, with attribution.
8. **No sponsor branding.** No Enefit, Eesti Energia or Kaggle logos, and no wording that suggests an affiliation or an official competition result.

*This document describes the author's good-faith approach to the data terms. It is not legal advice.*
