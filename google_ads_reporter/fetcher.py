"""Google Ads API calls — raw data only, no business logic."""

from typing import Any

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def get_campaign_stats(
    client: GoogleAdsClient,
    customer_id: str,
    start_date: str,
    end_date: str,
) -> list[dict[str, Any]]:
    """Fetch weekly campaign-level performance data for a single account.

    Args:
        client: An initialised GoogleAdsClient.
        customer_id: The Google Ads account ID.
        start_date: Start date in YYYY-MM-DD format.
        end_date: End date in YYYY-MM-DD format.

    Returns:
        A list of dicts with keys: campaign_id, campaign_name, impressions,
        clicks, cost_micros, conversions.

    Raises:
        RuntimeError: If the Google Ads API call fails.
    """
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions
        FROM campaign
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
    """

    try:
        response = ga_service.search_stream(
            customer_id=customer_id,
            query=query,
        )
    except GoogleAdsException as exc:
        raise RuntimeError(
            f"Google Ads API call failed for customer_id={customer_id}"
        ) from exc

    rows: list[dict[str, Any]] = []
    for batch in response:
        for row in batch.results:
            campaign = row.campaign
            metrics = row.metrics
            rows.append(
                {
                    "campaign_id": str(campaign.id),
                    "campaign_name": campaign.name,
                    "impressions": metrics.impressions,
                    "clicks": metrics.clicks,
                    "cost_micros": metrics.cost_micros,
                    "conversions": metrics.conversions,
                }
            )

    return rows