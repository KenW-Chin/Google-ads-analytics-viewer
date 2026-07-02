# Google Ads Reporter

A Python CLI tool that fetches the **last 8 weeks** of Google Ads campaign performance data and displays it as formatted tables in the terminal — one table per week, with the highest values highlighted in green.

---

## What it does

- **8-Week Reporting** — Automatically computes weekly ranges from the most recent Sunday going back 8 weeks (partial current week + 7 full Sunday→Saturday weeks).
- **Per-Week Tables** — Campaign name, Impressions, Clicks, CTR, Cost, CPC, and Conversions for every week.
- **Highlighted Leaders** — The highest Impressions, Clicks, CTR, and Conversions in each week's table are shown in bold green.
- **8-Week Totals** — Grand total spend and clicks across all 8 weeks at the bottom.
- **Multi-Account Support** — Loops over multiple Google Ads customer IDs and reports on each one.
- **Graceful Fallback** — If the API connection fails, it prints the error and falls back to the same mock data used by `--dry-run`, labelled so you know it's not live data.
- **Dry-Run Mode** — `--dry-run` skips the API entirely and displays 8 weeks of varied mock data.

---

## Requirements

- **Python 3.10+**
- A **Google Ads account** with API access (developer token, OAuth2 credentials)
- A **Google Cloud project** with the Google Ads API enabled

---

## Setup

### 1. Install dependencies

```bash
cd google_ads_reporter
pip install -r requirements.txt
```

### 2. Configure your `.env` file

Copy the example file and fill in your credentials:

```bash
cp .env.example .env
```

You'll need the following values (all obtained from your Google Cloud Console and Google Ads account):

| Variable | Description |
|----------|-------------|
| `GOOGLE_ADS_DEVELOPER_TOKEN` | Your Google Ads developer token |
| `GOOGLE_ADS_CLIENT_ID` | OAuth 2.0 client ID (Desktop app) |
| `GOOGLE_ADS_CLIENT_SECRET` | OAuth 2.0 client secret |
| `GOOGLE_ADS_REFRESH_TOKEN` | OAuth 2.0 refresh token (see below) |
| `GOOGLE_ADS_LOGIN_CUSTOMER_ID` | Your manager account ID (digits only) |
| `GOOGLE_ADS_CUSTOMER_IDS` | Comma-separated client account IDs to report on |

### 3. Obtain a refresh token

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create or select a project, then **enable the Google Ads API**.
3. Under **APIs & Services > Credentials**, create an **OAuth 2.0 Client ID** (Desktop app).
4. Copy the **Client ID** and **Client Secret** into your `.env` file.
5. Install and run `google-ads-auth` to generate a refresh token:

   ```bash
   pip install google-ads-auth
   google-ads-auth \
     --client-id YOUR_CLIENT_ID \
     --client-secret YOUR_CLIENT_SECRET \
     --developer-token YOUR_DEVELOPER_TOKEN \
     --login-customer-id YOUR_LOGIN_CUSTOMER_ID \
     --scopes https://www.googleapis.com/auth/adwords
   ```

6. Copy the resulting refresh token into your `.env` file.

---

## Usage

### Quick start — no API required

```bash
python ./google_ads_reporter/main.py --dry-run
```

This uses built-in mock data spanning 8 weeks and shows the full report.

### Live report

```bash
python ./google_ads_reporter/main.py
```

Fetches real data from the Google Ads API for each account in `GOOGLE_ADS_CUSTOMER_IDS`. If the API is not configured or fails, mock data is shown with a clear label.

### Override accounts on the fly

```bash
python ./google_ads_reporter/main.py --accounts 1234567890,0987654321
```

---

## Project structure

```
google_ads_reporter/
├── .env                    # Your credentials (never committed)
├── .env.example            # Template showing required environment variables
├── requirements.txt        # Pinned Python dependencies
├── config.py               # Loads settings from .env & computes 8 weekly date ranges
├── fetcher.py              # Google Ads API queries — one call per week
├── processor.py            # Converts micros → dollars, computes CTR/CPC, filters, sorts
├── reporter.py             # Renders rich tables with highlighted best values + totals
├── mock_data.py            # 8 weeks of mock campaign data for dry-run / API fallback
├── main.py                 # Entry point — CLI args, orchestration, error handling
└── README.md               # This file
```

## File overview

| File | Purpose |
|------|---------|
| `config.py` | Loads credentials from `.env` and computes 8 weekly date ranges (last Sunday → today, then 7 full Sun→Sat weeks back). |
| `fetcher.py` | Makes one Google Ads API query per week, tags each row with `week_start`/`week_end`. |
| `processor.py` | Transforms raw data — converts `cost_micros` to dollars, computes CTR and CPC, filters zero-impression rows, sorts by cost. |
| `reporter.py` | Renders one rich Table per week with bold green highlighting on the highest Impressions, Clicks, CTR, and Conversions. Shows per-week totals and an 8-week grand total. |
| `mock_data.py` | Stores 8 weeks of sample campaign data used by `--dry-run` and when the API is unreachable. |
| `main.py` | Parses CLI arguments (`--dry-run`, `--accounts`), orchestrates fetcher → processor → reporter per account, and falls back to mock data if the API fails. |