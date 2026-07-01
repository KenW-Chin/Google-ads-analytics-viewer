# Google Ads Reporter

A simple CLI tool that fetches weekly Google Ads campaign performance data and displays formatted tables in the terminal.

## Setup

1. **Install dependencies:**

   ```bash
   cd google_ads_reporter
   pip install -r requirements.txt
   ```

2. **Set up your `.env` file:**

   Copy `.env.example` to `.env` and fill in your credentials:

   ```bash
   cp .env.example .env
   ```

3. **Get a refresh token:**

   To authenticate with the Google Ads API you need OAuth2 credentials and a refresh token:

   1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
   2. Create a project (or select an existing one) and enable the **Google Ads API**.
   3. Under **APIs & Services > Credentials**, create an **OAuth 2.0 Client ID** (Desktop app).
   4. Copy the **Client ID** and **Client Secret** into your `.env` file.
   5. Use a tool like [google-ads-auth](https://pypi.org/project/google-ads-auth/) to obtain a refresh token:
      ```bash
      pip install google-ads-auth
      google-ads-auth --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET --developer-token YOUR_DEVELOPER_TOKEN --login-customer-id YOUR_LOGIN_CUSTOMER_ID --scopes https://www.googleapis.com/auth/adwords
      ```
   6. Copy the resulting refresh token into your `.env` file.

4. **Set your account IDs:**

   - `GOOGLE_ADS_LOGIN_CUSTOMER_ID` — your manager account ID (numbers only).
   - `GOOGLE_ADS_CUSTOMER_IDS` — comma-separated list of client account IDs to report on.

## Usage

**Dry run** (no API call, uses mock data):

```bash
python main.py --dry-run
```

**Live run** (fetches real data from Google Ads):

```bash
python main.py
```

**With custom date range:**

```bash
python main.py --start-date 2026-06-01 --end-date 2026-06-07
```

**Override accounts from the command line:**

```bash
python main.py --accounts 1234567890,0987654321
```

## File overview

| File | Purpose |
|------|---------|
| `config.py` | Loads all credentials and settings from environment variables. |
| `fetcher.py` | Makes the Google Ads API call and returns raw campaign data. |
| `processor.py` | Transforms raw data — converts micros to dollars, computes CTR/CPC, filters and sorts. |
| `reporter.py` | Renders a formatted table and summary line using the `rich` library. |
| `main.py` | Entry point that parses CLI arguments and orchestrates the pipeline. |