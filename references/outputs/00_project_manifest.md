# Dataset Setup & Statistical Hygiene Report — B2B SaaS Customer Intelligence Study 2026

**Total Sample ($N$):** `240` · **Effective Sample ($N_{\text{eff}}$):** `239.1` (DEFF = `1.00`) · **Global 95% CI MoE:** `±6.34%`

> **Margin Note:** Global Margin of Error is computed at the 95% confidence level ($z = 1.96$) under maximum binomial variance ($p = 0.50$). Subgroup margins widen proportionally to $1/\sqrt{n_{\text{sub}}}$.

## 1. Article 6 Data Quality Gates Audit

| Quality Gate | Constitutional Rule | Result | Audit Diagnostic |
| :--- | :--- | :--- | :--- |
| **Gate 6a: Straight-Lining** | Row SD $= 0$ across $\ge 5$ Likert items | `EVALUATED` | `0` respondents (`0.0%`) · Sensitivity $\Delta = 0.0%` |
| **Gate 6b: Percentage Sums** | Category distributions sum to $100\% \pm 0.5\%$ | `PASS` | `0` violations across `4` categorical variables |
| **Gate 6c: Missingness Rate** | Flag variables $>10\%$ and $>20\%$ missing | `CAVEAT` | `0` moderate ($>10\%$), `3` high ($>20\%$) missingness columns |

## 2. Quantitative & Likert Scale Variable Profile

| Variable | Role | Valid $N$ | Mean ± 95% MoE | SD | Median (IQR) | Skewness | Top-2-Box % | Estimator |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| **Product Quality** (`product_quality`) | likert | 240 | 3.71 (±0.12) | 0.94 | 4.00 (1.00) | -0.26 | 58.8% | Parametric (Mean/SD) |
| **Support Speed** (`support_speed`) | likert | 240 | 2.89 (±0.13) | 1.03 | 3.00 (2.00) | +0.13 | 25.4% | Parametric (Mean/SD) |
| **Pricing Value** (`pricing_value`) | likert | 240 | 2.73 (±0.13) | 1.03 | 3.00 (1.00) | +0.20 | 20.4% | Parametric (Mean/SD) |
| **Onboarding UX** (`onboarding_ux`) | likert | 240 | 3.50 (±0.12) | 0.96 | 3.00 (1.00) | -0.03 | 48.3% | Parametric (Mean/SD) |
| **API Stability** (`api_stability`) | likert | 240 | 3.93 (±0.10) | 0.82 | 4.00 (2.00) | -0.19 | 68.8% | Parametric (Mean/SD) |
| **Overall Satisfaction** (`overall_satisfaction`) | likert | 240 | 3.19 (±0.11) | 0.87 | 3.00 (1.00) | -0.03 | 35.0% | Parametric (Mean/SD) |
| **Recommendation Score** (`recommendation_score`) | likert | 240 | 6.65 (±0.26) | 2.03 | 7.00 (3.00) | -0.41 | 18.8% | Parametric (Mean/SD) |

## 3. Categorical & Segment Distributions

| Variable | Valid $N$ | Missing % | Unique Categories | Top Modal Category (Count, % ± 95% MoE) |
| :--- | ---: | ---: | ---: | :--- |
| **Customer Segment** (`customer_segment`) | 240 | 0.0% | 4 | Mid-Market (`n=84`, `35.0% ±6.0%`) |
| **Region** (`region`) | 240 | 0.0% | 4 | Southeast (`n=105`, `43.8% ±6.3%`) |
| **Enterprise SLA Status** (`enterprise_sla_status`) | 63 | 73.8% | 2 | Met SLA (`n=52`, `82.5% ±9.4%`) |
| **SMB Self-Serve Funnel** (`smb_self_serve_funnel`) | 66 | 72.5% | 2 | Completed (`n=41`, `62.1% ±11.7%`) |

## 4. Open-Ended Qualitative Verbatim Channels

| Open-Text Column | Valid Verbatims ($N$) | Missing % | Mean Length (chars) |
| :--- | ---: | ---: | ---: |
| **Open Feedback** (`open_feedback`) | 22 | 90.8% | 63.3 |
