from unittest.mock import patch
import pytest
from asset import Asset


@patch("cbr.get_usd_course")
def test_can_mock_external_calls(mock_get_usd_course):
##code##
    mock_get_usd_course.side_effect = [76.32, 77.44, ConnectionError]

    asset_property = Asset(name="property", capital=10**6, interest=0.1)
    for iteration in range(0, 2, 2):
        expected_revenue = (76.32 + 0.1 * iteration) * asset_property.capital * asset_property.interest
        calculated_revenue = asset_property.calculate_revenue_from_usd(years=1)
        assert calculated_revenue == pytest.approx(expected_revenue, abs=0.01), (
            f"incorrect calculated revenue at iteration {iteration}"
            )
