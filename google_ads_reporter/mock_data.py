"""Mock data for dry-run and API fallback scenarios.

Each inner list corresponds to one weekly range of campaign data.
week_start/week_end are assigned dynamically at runtime.
"""

# 8 weeks of mock campaign data — one list per week
DRY_RUN_WEEKLY_DATA: list[list[dict]] = [
    # Week 1: Brand, Competitor, Generic
    [
        {"campaign_id": "1", "campaign_name": "Brand", "impressions": 10000, "clicks": 420, "cost_micros": 50000000, "conversions": 18},
        {"campaign_id": "2", "campaign_name": "Competitor", "impressions": 8000, "clicks": 200, "cost_micros": 30000000, "conversions": 5},
        {"campaign_id": "3", "campaign_name": "Generic", "impressions": 500, "clicks": 0, "cost_micros": 0, "conversions": 0},
    ],
    # Week 2
    [
        {"campaign_id": "1", "campaign_name": "Brand", "impressions": 10500, "clicks": 440, "cost_micros": 52000000, "conversions": 20},
        {"campaign_id": "2", "campaign_name": "Competitor", "impressions": 7500, "clicks": 190, "cost_micros": 28000000, "conversions": 4},
        {"campaign_id": "3", "campaign_name": "Generic", "impressions": 600, "clicks": 5, "cost_micros": 2000000, "conversions": 1},
    ],
    # Week 3
    [
        {"campaign_id": "1", "campaign_name": "Brand", "impressions": 9800, "clicks": 410, "cost_micros": 49000000, "conversions": 17},
        {"campaign_id": "2", "campaign_name": "Competitor", "impressions": 8200, "clicks": 210, "cost_micros": 31000000, "conversions": 6},
    ],
    # Week 4
    [
        {"campaign_id": "1", "campaign_name": "Brand", "impressions": 11000, "clicks": 450, "cost_micros": 55000000, "conversions": 22},
        {"campaign_id": "2", "campaign_name": "Competitor", "impressions": 7200, "clicks": 180, "cost_micros": 27000000, "conversions": 3},
    ],
    # Week 5
    [
        {"campaign_id": "1", "campaign_name": "Brand", "impressions": 10200, "clicks": 430, "cost_micros": 51000000, "conversions": 19},
        {"campaign_id": "3", "campaign_name": "Generic", "impressions": 700, "clicks": 8, "cost_micros": 3000000, "conversions": 2},
    ],
    # Week 6
    [
        {"campaign_id": "1", "campaign_name": "Brand", "impressions": 9500, "clicks": 400, "cost_micros": 48000000, "conversions": 16},
        {"campaign_id": "2", "campaign_name": "Competitor", "impressions": 8500, "clicks": 220, "cost_micros": 32000000, "conversions": 7},
    ],
    # Week 7
    [
        {"campaign_id": "1", "campaign_name": "Brand", "impressions": 10800, "clicks": 445, "cost_micros": 53000000, "conversions": 21},
        {"campaign_id": "3", "campaign_name": "Generic", "impressions": 650, "clicks": 6, "cost_micros": 2500000, "conversions": 1},
    ],
    # Week 8
    [
        {"campaign_id": "1", "campaign_name": "Brand", "impressions": 9900, "clicks": 415, "cost_micros": 49500000, "conversions": 18},
        {"campaign_id": "2", "campaign_name": "Competitor", "impressions": 7800, "clicks": 195, "cost_micros": 29000000, "conversions": 5},
    ],
]