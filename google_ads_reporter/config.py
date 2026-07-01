"""Load all credentials and settings from environment variables."""

import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()


def _compute_default_date_range() -> tuple[str, str]:
    """Return (start_date, end_date) for the last 7 days as YYYY-MM-DD strings."""
    end = datetime.now()
    start = end - timedelta(days=7)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


def load_config() -> dict:
    """Load and return all configuration values from environment variables."""
    customer_ids_raw = os.getenv("GOOGLE_ADS_CUSTOMER_IDS", "")
    customer_ids = [cid.strip() for cid in customer_ids_raw.split(",") if cid.strip()]

    start_date, end_date = _compute_default_date_range()

    return {
        "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN", ""),
        "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID", ""),
        "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET", ""),
        "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN", ""),
        "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID", ""),
        "customer_ids": customer_ids,
        "date_range": {
            "start": start_date,
            "end": end_date,
        },
    }