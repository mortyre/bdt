from unittest.mock import patch, MagicMock
import pytest
from asset import print_asset_revenue

@pytest.fixture
def asset_filepath(tmpdir):
    asset_fileio = tmpdir.join("asset.txt")
    asset_fileio.write("property 1000000 0.1")
    asset_filepath_ = asset_fileio.strpath
    return asset_filepath_

@patch("asset.Asset")
def test_asset_calculate_revenue_always_return_100500(mock_asset_class,asset_filepath, capsys):
    ##code##
    #mock_asset_class = MagicMock()
    mock_asset_class.calculate_revenue.return_value = 100500.0
    mock_asset_class.build_from_str.return_value.calculate_revenue.return_value = 100500.0
    #asset_filepath = asset_filepath()

    periods = [1, 2, 5, 10]
    with open(asset_filepath) as asset_fin:
        print(asset_fin)
        print_asset_revenue(asset_fin, periods=periods)
    captured = capsys.readouterr()
