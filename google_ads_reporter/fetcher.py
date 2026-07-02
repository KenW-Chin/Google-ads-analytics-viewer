"""Google Ads API calls — raw data only, no business logic."""

from typing import Any

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def get_campaign_stats(
    client: GoogleAdsClient,
    customer_id: str,
    weekly_ranges: list[tuple[str, str]],
) -> list[dict[str, Any]]:
    """Fetch campaign-level performance data across multiple weekly ranges.

    For each (start_date, end_date) pair, a separate API query is made and
    each returned row is tagged with ``week_start`` and ``week_end`` so the
    caller can group results by week.

    Args:
        client: An initialised GoogleAdsClient.
        customer_id: The Google Ads account ID.
        weekly_ranges: List of (start_date, end_date) tuples in YYYY-MM-DD
            format, most recent first.

    Returns:
        A list of dicts with keys: campaign_id, campaign_name, impressions,
        clicks, cost_micros, conversions, week_start, week_end.

    Raises:
        RuntimeError: If the Google Ads API call fails for any week.
    """
    ga_service = client.get_service("GoogleAdsService")

    all_rows: list[dict[str, Any]] = []

    for week_start, week_end in weekly_ranges:
        query = f"""
            SELECT
                campaign.id,
                campaign.name,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions
            FROM campaign
            WHERE segments.date BETWEEN '{week_start}' AND '{week_end}'
        """

        try:
            response = ga_service.search_stream(
                customer_id=customer_id,
                query=query,
            )
        except GoogleAdsException as exc:
            raise RuntimeError(
                f"Google Ads API call failed for customer_id={customer_id}, "
                f"week={week_start} to {week_end}"
            ) from exc

        for batch in response:
            for row in batch.results:
                campaign = row.campaign
                metrics = row.metrics
                all_rows.append(
                    {
                        "campaign_id": str(campaign.id),
                        "campaign_name": campaign.name,
                        "impressions": metrics.impressions,
                        "clicks": metrics.clicks,
                        "cost_micros": metrics.cost_micros,
                        "conversions": metrics.conversions,
                        "week_start": week_start,
                        "week_end": week_end,
                    }
                )

    return all_rows