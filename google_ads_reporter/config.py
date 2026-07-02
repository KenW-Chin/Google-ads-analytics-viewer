"""Load all credentials and settings from environment variables."""

import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()


def _compute_weekly_date_ranges() -> list[tuple[str, str]]:
    """Compute 8 weekly date ranges ending on the most recent Sunday.

    Week 1: the partial current week (last Sunday → today).
    Weeks 2–8: full Sunday→Saturday weeks going back from there.

    Returns:
        List of (start_date, end_date) tuples, most recent first.
    """
    today = datetime.now()

    # How many days since the most recent Sunday?
    # Python weekday(): Monday=0, Sunday=6
    days_since_sunday = today.weekday() + 1  # Mon=1, Tue=2, …, Sun=7
    if days_since_sunday == 7:
        days_since_sunday = 0  # today is Sunday itself

    last_sunday = today - timedelta(days=days_since_sunday)

    ranges: list[tuple[str, str]] = []

    # Week 1: last Sunday → today (current partial week)
    ranges.append((last_sunday.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")))

    # Weeks 2–8: full Sunday→Saturday weeks going back
    for _ in range(1, 8):
        week_end = last_sunday - timedelta(days=1)          # previous Saturday
        week_start = week_end - timedelta(days=6)            # previous Sunday
        ranges.append((week_start.strftime("%Y-%m-%d"), week_end.strftime("%Y-%m-%d")))
        last_sunday = week_start  # move back one full week

    return ranges


def load_config() -> dict:
    """Load and return all configuration values from environment variables."""
    customer_ids_raw = os.getenv("GOOGLE_ADS_CUSTOMER_IDS", "")
    customer_ids = [cid.strip() for cid in customer_ids_raw.split(",") if cid.strip()]

    return {
        "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN", ""),
        "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID", ""),
        "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET", ""),
        "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN", ""),
        "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID", ""),
        "customer_ids": customer_ids,
        "weekly_date_ranges": _compute_weekly_date_ranges(),
    }