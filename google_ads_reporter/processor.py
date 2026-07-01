"""Data transformation and computation."""

from typing import Any


def process(raw_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Transform raw API data into a cleaned, computed list of dicts.

    Steps:
      1. Convert cost_micros to dollars (rounded to 2 decimal places).
      2. Compute CTR = clicks / impressions (default 0.0 if zero impressions).
      3. Compute CPC = cost / clicks (default 0.0 if zero clicks).
      4. Filter out rows where impressions == 0.
      5. Sort by cost descending.

    Args:
        raw_rows: List of dicts from the fetcher.

    Returns:
        Cleaned list of dicts with keys: campaign_name, impressions, clicks,
        cost, ctr, cpc, conversions.
    """
    processed: list[dict[str, Any]] = []

    for row in raw_rows:
        impressions = row["impressions"]
        clicks = row["clicks"]
        cost_micros = row["cost_micros"]

        # Filter out zero-impression rows
        if impressions == 0:
            continue

        cost = round(cost_micros / 1_000_000, 2)

        # CTR = clicks / impressions
        ctr = round(clicks / impressions, 4) if impressions > 0 else 0.0

        # CPC = cost (in dollars) / clicks
        cpc = round(cost / clicks, 2) if clicks > 0 else 0.0

        processed.append(
            {
                "campaign_name": row["campaign_name"],
                "impressions": impressions,
                "clicks": clicks,
                "cost": cost,
                "ctr": ctr,
                "cpc": cpc,
                "conversions": row["conversions"],
            }
        )

    # Sort by cost descending
    processed.sort(key=lambda r: r["cost"], reverse=True)

    return processed