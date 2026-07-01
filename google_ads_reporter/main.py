"""Entry point — orchestrates the pipeline: fetcher → processor → reporter."""

import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient

from config import load_config
from fetcher import get_campaign_stats
from processor import process
from reporter import print_report, print_error

DRY_RUN_DATA = [
    {
        "campaign_id": "1",
        "campaign_name": "Brand",
        "impressions": 10000,
        "clicks": 420,
        "cost_micros": 50000000,
        "conversions": 18,
    },
    {
        "campaign_id": "2",
        "campaign_name": "Competitor",
        "impressions": 8000,
        "clicks": 200,
        "cost_micros": 30000000,
        "conversions": 5,
    },
    {
        "campaign_id": "3",
        "campaign_name": "Generic",
        "impressions": 500,
        "clicks": 0,
        "cost_micros": 0,
        "conversions": 0,
    },
]


def parse_args() -> argparse.Namespace:
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch and display weekly Google Ads campaign performance."
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default=None,
        help="Start date (YYYY-MM-DD). Defaults to 7 days ago.",
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


def main() -> None:
    """Main entry point."""
    args = parse_args()
    config = load_config()

    # Override date range from CLI if provided
    start_date = args.start_date or config["date_range"]["start"]
    end_date = args.end_date or config["date_range"]["end"]

    # Override accounts from CLI if provided
    if args.accounts:
        customer_ids = [cid.strip() for cid in args.accounts.split(",") if cid.strip()]
    else:
        customer_ids = config["customer_ids"]

    # Print header
    print(f"Weekly Google Ads Report: {start_date} to {end_date}")
    print("=" * 60)

    if args.dry_run:
        # Process and display mock data for one account
        account_id = "DRY-RUN-ACCOUNT"
        rows = process(DRY_RUN_DATA)
        print_report(account_id, rows, start_date, end_date)
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
        print_error("N/A", f"Failed to initialise Google Ads client: {exc}")
        sys.exit(1)

    # Loop over all customer IDs
    for customer_id in customer_ids:
        try:
            raw_rows = get_campaign_stats(client, customer_id, start_date, end_date)
            rows = process(raw_rows)
            print_report(customer_id, rows, start_date, end_date)
        except Exception as exc:
            print_error(customer_id, str(exc))
            # Continue with the next account


if __name__ == "__main__":
    main()