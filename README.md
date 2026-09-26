# 🎮 Clash Royale Game Analytics

> **What makes players stay, play, and spend?**

An end-to-end **mobile game analytics project** focused on understanding player engagement, retention, monetization, segmentation, and platform behavior.

The project started as a Python-based exploratory analysis and was later transformed into an **interactive Streamlit dashboard** designed to communicate analytical findings through a presentation-style product analytics experience.

🔗 **[Explore the Interactive Dashboard](https://clash-royale-analysis-dashboard.streamlit.app/)**

---

## 🎯 Business Question

For a mobile game, understanding **what makes players stay, play, and spend** is essential for improving player experience and business performance.

This project explores:

* How do players engage with the game?
* What does early player behavior tell us about future retention?
* How does engagement relate to monetization?
* How do different player segments behave?
* Are there meaningful differences between Android and iOS players?
* What business actions could be tested based on these patterns?

---

## 📊 Dataset

The analysis uses a public Clash Royale dataset from the repository created by **[Melih Kurtaran](https://github.com/melihkurtaran/Clash_Royale)**.

The dataset contains three main tables:

### `account`

Player-level information including:

* `account_id`
* `created_time`
* `created_device`
* `created_platform`
* `country_code`
* `created_app_store_id`

### `account_date_session`

Daily player activity including:

* `account_id`
* `date`
* `session_count`
* `session_duration_sec`

### `iap_purchase`

In-app purchase information including:

* `account_id`
* `created_time`
* `package_id_hash`
* `iap_price_usd_cents`
* `app_store_id`

### Dataset Size

| Table          |      Rows |
| -------------- | --------: |
| Account        |   112,792 |
| Daily Sessions | 1,698,974 |
| IAP Purchases  |     9,909 |

---

# 🔎 Analysis

The project follows this analytical flow:

**SQLite → Data Cleaning → Exploratory Analysis → Engagement → Retention → Monetization → Segmentation → Platform Analysis → Business Insights → Dashboard**

---

## 1. 🎮 Player Engagement

The first step was understanding how players interact with the game.

Key metrics included:

* Sessions per player-day
* Session duration
* Average and median engagement
* Engagement distributions
* Platform-level engagement

### Key observations

The session distribution was right-skewed:

* Mean sessions: **3.59**
* Median sessions: **2**

Play time was also right-skewed:

* Mean play time: **23.9 minutes**
* Median play time: **14.4 minutes**

This means that while some player-days contain very high activity, most player-days are concentrated around relatively low session counts and shorter play durations.

---

# 2. 🔄 Retention Analysis

Retention was analyzed at several milestones:

* D1
* D7
* D14
* D30

Overall retention declined as the time from acquisition increased.

The analysis also included **cohort retention**, allowing retention behavior to be compared across different signup cohorts.

### Retention approach

Players were considered on Day 0 based on their creation date.

The dataset contains a small number of inconsistencies between account creation dates and first recorded session dates, so these were investigated rather than silently removed.

---

# 3. 📈 Early Engagement → D7 Retention

One of the most important findings came from comparing **Day-0 session activity** with D7 retention.

Players were grouped into four engagement segments:

| Engagement Segment | D7 Retention |
| ------------------ | -----------: |
| 1 session          |     **8.1%** |
| 2 sessions         |    **22.7%** |
| 3–4 sessions       |    **36.0%** |
| 5+ sessions        |    **55.3%** |

There is a strong observed association between higher early engagement and higher D7 retention.

### Important

This is an **observational relationship, not a causal conclusion**.

Higher engagement does not necessarily cause higher retention. Further analysis and controlled experiments would be required to identify causal drivers.

---

# 4. 💰 Monetization

Monetization was analyzed using:

* Payer conversion
* Revenue
* ARPU
* ARPPU
* Revenue contribution by engagement segment

### Engagement and monetization

Higher Day-0 engagement was associated with higher payer conversion and ARPU.

At the same time, **ARPPU was comparatively more stable** across engagement groups.

This suggests an interesting business question:

> Is the larger monetization opportunity primarily increasing the number of players who convert, rather than significantly increasing spend among existing payers?

This would be an important hypothesis to test with more detailed purchase and player-lifecycle data.

---

# 5. 👥 Player Segmentation

Players were segmented based on their **Day-0 session count**:

| Segment              | Definition   |
| -------------------- | ------------ |
| Low Engagement       | 1 session    |
| Moderate Engagement  | 2 sessions   |
| High Engagement      | 3–4 sessions |
| Very High Engagement | 5+ sessions  |

### Segment sizes

| Segment   | Players | Share |
| --------- | ------: | ----: |
| Low       |  65,389 | 58.0% |
| Moderate  |  18,376 | 16.3% |
| High      |  14,510 | 12.9% |
| Very High |  14,176 | 12.6% |

The segments show substantial differences in D7 retention and monetization behavior.

The **Very High Engagement** segment represents a relatively small portion of the player base but shows substantially higher observed retention, payer conversion, and ARPU.

This creates a useful product question:

> How can the game increase meaningful early engagement across a broader portion of the player base?

---

# 6. 📱 Platform Analysis

Android and iOS players were compared across:

* Player volume
* Session activity
* Play time
* D1 retention
* D7 retention
* Payer conversion
* ARPU
* ARPPU

### Selected results

| Metric           | Android |    iOS |
| ---------------- | ------: | -----: |
| D1 Retention     |  39.80% | 39.38% |
| D7 Retention     |  19.49% | 22.58% |
| Payer Conversion |   1.25% |  1.95% |
| ARPU             |   $0.27 |  $0.85 |
| ARPPU            |  $21.88 | $43.56 |

Android represents the majority of the observed player base, while iOS shows higher observed D7 retention and monetization metrics in this dataset.

These differences should be investigated further before attributing them to platform-specific causes.

---

# 💡 Business Insights & Potential Actions

The analysis led to several potential product and business hypotheses.

### 1. Improve early-game engagement

Investigate:

* Onboarding
* First-session experience
* Early quests
* Rewards
* Progression
* Initial player goals

The goal would be to understand which experiences are associated with stronger early engagement.

### 2. Identify early churn risk

Players with very low Day-0 activity could be studied as a potential early-retention opportunity.

Possible experiments could include:

* Personalized rewards
* Re-engagement campaigns
* Early progression adjustments
* Reminder mechanisms

### 3. Connect engagement and monetization

Rather than analyzing monetization independently, investigate how engagement milestones relate to purchase behavior.

Potential experiments could focus on:

* Offer timing
* Offer personalization
* Purchase flow
* Monetization experiences for highly engaged players

### 4. Investigate platform differences

The Android/iOS differences raise questions around:

* Purchase flow
* Pricing
* Offers
* Player behavior
* Platform-specific user experience

These should be investigated using more detailed data and controlled experiments.

---

# 🖥️ Interactive Streamlit Dashboard

One of the main goals of the project was to transform the analytical work into an interactive presentation.

This was also my **first experience building a dashboard with Streamlit**, making the dashboard itself a new technical challenge.

The analytical outputs were rebuilt as interactive visualizations and organized into six sections:

### 🏟️ Overview

High-level view of:

* Player base
* DAU
* Retention
* Revenue
* Platform mix

### 🎮 Engagement

Explores:

* Session frequency
* Play time
* Engagement distribution
* Engagement → retention relationship

### 🔄 Retention

Includes:

* Retention milestones
* Cohort analysis
* Retention trends
* Engagement → D7 retention

### 💰 Monetization

Includes:

* Revenue
* Payer conversion
* ARPU
* ARPPU
* Monetization by engagement

### 👥 Player Segmentation

Explores:

* Player segment sizes
* D7 retention by segment
* Revenue contribution
* ARPU / ARPPU
* Payer conversion

### 📱 Platform Analysis

Compares:

* Android vs. iOS
* Engagement
* Retention
* Monetization

---

## 🚀 Dashboard

👉 **[Open the Interactive Streamlit Dashboard](https://clash-royale-analysis-dashboard.streamlit.app/)**

---

# 🛠️ Tech Stack

### Data & Analysis

* Python
* Pandas
* NumPy
* SQLite

### Visualization

* Plotly
* Matplotlib
* Seaborn

### Dashboard

* Streamlit
* HTML/CSS customization

### Development Assistance

* ChatGPT
* Gemini

AI tools were used as development assistants for implementation ideas, debugging, UI refinement, and iteration.

---

# 🤝 Acknowledgements

### Dataset

Special thanks to **[Melih Kurtaran](https://github.com/melihkurtaran/Clash_Royale)** for creating and publicly sharing the dataset used in this project.

### Dashboard & Deployment

Special thanks to [Saeed Mansourian](https://www.linkedin.com/in/saeed-mansourian/) for helping with:

* Frontend/presentation design
* Dashboard interface refinement
* Streamlit deployment
* Getting the application up and running

---

# 📌 Project Takeaway

The main goal of this project was not simply to create charts.

It was to practice the complete analytics journey:

> **Data → Analysis → Finding → Business Insight → Action → Presentation**

The project combines **game analytics, product thinking, data visualization, Python, and interactive dashboard development** into one end-to-end portfolio project.

---

## 📬 Connect

If you're interested in **Game Analytics, Product Analytics, Business Intelligence, or Data Analysis**, I'd be happy to connect and discuss the project.

🌐 **Portfolio:**
https://kimiaderazgisoo.github.io/

🔗 **Interactive Dashboard:**
https://clash-royale-analysis-dashboard.streamlit.app/
