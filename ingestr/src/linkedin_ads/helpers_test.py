import pendulum

from ingestr.src.linkedin_ads.helpers import find_intervals, flat_structure


def test_flat_structure_linkedin_ads():
    items_daily = [
        {
            "clicks": 0,
            "impressions": 43,
            "pivotValues": [
                "urn:li:sponsoredCampaign:123456",
            ],
            "dateRange": {
                "start": {"month": 12, "day": 10, "year": 2024},
                "end": {"month": 12, "day": 10, "year": 2024},
            },
            "likes": 0,
        }
    ]

    expected_output_daily = [
        {
            "clicks": 0,
            "impressions": 43,
            "campaign": "urn:li:sponsoredCampaign:123456",
            "date": "2024-12-10",
            "likes": 0,
        }
    ]
    assert flat_structure(items_daily, "CAMPAIGN", "DAILY") == expected_output_daily

    items_monthly = [
        {
            "clicks": 0,
            "impressions": 43,
            "pivotValues": [
                "urn:li:sponsoredCampaign:123456",
                "urn:li:sponsoredCampaign:7891011",
            ],
            "dateRange": {
                "start": {"month": 12, "day": 10, "year": 2024},
                "end": {"month": 12, "day": 30, "year": 2024},
            },
            "likes": 0,
        }
    ]
    expected_output_monthly = [
        {
            "clicks": 0,
            "impressions": 43,
            "campaign": "urn:li:sponsoredCampaign:123456, urn:li:sponsoredCampaign:7891011",
            "start_date": "2024-12-10",
            "end_date": "2024-12-30",
            "likes": 0,
        }
    ]

    assert (
        flat_structure(items_monthly, "CAMPAIGN", "MONTHLY") == expected_output_monthly
    )


def test_find_intervals_linkedin_ads():
    start_date = pendulum.date(2024, 1, 1)
    end_date = pendulum.date(2024, 12, 31)
    assert find_intervals(start_date, end_date, "MONTHLY") == [
        (pendulum.date(2024, 1, 1), pendulum.date(2024, 12, 31))
    ]

    assert find_intervals(
        pendulum.date(2020, 1, 1), pendulum.date(2024, 12, 31), "MONTHLY"
    ) == [
        (pendulum.date(2020, 1, 1), pendulum.date(2022, 1, 1)),
        (pendulum.date(2022, 1, 2), pendulum.date(2024, 1, 2)),
        (pendulum.date(2024, 1, 3), pendulum.date(2024, 12, 31)),
    ]

    assert find_intervals(
        pendulum.date(2022, 2, 1), pendulum.date(2024, 2, 8), "MONTHLY"
    ) == [
        (pendulum.date(2022, 2, 1), pendulum.date(2024, 2, 1)),
        (pendulum.date(2024, 2, 2), pendulum.date(2024, 2, 8)),
    ]

    assert find_intervals(
        pendulum.date(2023, 1, 1), pendulum.date(2024, 12, 20), "DAILY"
    ) == [
        (pendulum.date(2023, 1, 1), pendulum.date(2023, 7, 1)),
        (pendulum.date(2023, 7, 2), pendulum.date(2024, 1, 2)),
        (pendulum.date(2024, 1, 3), pendulum.date(2024, 7, 3)),
        (pendulum.date(2024, 7, 4), pendulum.date(2024, 12, 20)),
    ]
