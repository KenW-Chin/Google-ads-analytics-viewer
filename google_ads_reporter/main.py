"""Entry point — orchestrates the pipeline: fetcher → processor → reporter."""

import argparse
import sys
from rich.console import Console

from google.ads.googleads.client import GoogleAdsClient

from config import load_config
from fetcher import get_campaign_stats
from mock_data import DRY_RUN_WEEKLY_DATA
from processor import process
from reporter import print_report, print_error


def parse_args() -> argparse.Namespace:
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch and display weekly Google Ads campaign performance."
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default=None,
        help="Start date (YYYY-MM-DD). Defaults to 8 weeks ago.",
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default=None,
        help="End date (YYYY-MM-DD). Defaults to today.",
    )
    parser.add_argument(
        "--accounts",
        type=str,
        default=None,
        help="Comma-separated list of account IDs (overrides config).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip API call and use mock data for one account.",
    )
    return parser.parse_args()


def _build_dry_run_rows(
    weekly_ranges: list[tuple[str, str]],
) -> list[dict]:
    """Build a flat list of dicts tagged with week_start/week_end from data."""
    rows: list[dict] = []
    for i, (week_start, week_end) in enumerate(weekly_ranges):
        for week_row in DRY_RUN_WEEKLY_DATA[i]:
            row = dict(week_row)
            row["week_start"] = week_start
            row["week_end"] = week_end
            rows.append(row)
    return rows


def main() -> None:
    """Main entry point."""
    args = parse_args()
    # Obtain all APIs
    config = load_config()
    console = Console()

    weekly_ranges = config["weekly_date_ranges"]

    # Override accounts from CLI if provided under --accounts
    if args.accounts:
        customer_ids = [cid.strip() for cid in args.accounts.split(",") if cid.strip()]
    else:
        customer_ids = config["customer_ids"]

    # Print header
    overall_start = weekly_ranges[-1][0] if weekly_ranges else "?"
    overall_end = weekly_ranges[0][1] if weekly_ranges else "?"
    console.print(f"Weekly Google Ads Report (8 weeks): {overall_start} to {overall_end}")
    console.print("=" * 70)

    # Handle dry-run mode (Get mock data)
    if args.dry_run:
        account_id = "DRY-RUN-ACCOUNT"
        raw_rows = _build_dry_run_rows(weekly_ranges)
        rows = process(raw_rows)
        print_report(account_id, rows, weekly_ranges)
        return

    if not customer_ids:
        print_error(
            "N/A",
            "No customer IDs found. Set GOOGLE_ADS_CUSTOMER_IDS in .env or pass --accounts.",
        )
        sys.exit(1)

    # Initialise the Google Ads client once
    try:
        client = GoogleAdsClient.load_from_env()
    except Exception as exc:
        print_error("N/A", f"Could not connect to Google Ads API: {exc}")
        return

    # Loop over all customer IDs
    for customer_id in customer_ids:
        try:
            raw_rows = get_campaign_stats(client, customer_id, weekly_ranges)
            rows = process(raw_rows)
            print_report(customer_id, rows, weekly_ranges)
        except Exception as exc:
            print_error(customer_id, f"Could not connect to Google Ads API: {exc}")


if __name__ == "__main__":
    main()