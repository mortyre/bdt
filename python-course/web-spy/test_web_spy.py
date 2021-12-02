import pytest
from argparse import Namespace
from unittest.mock import patch
import requests

from task_web_spy import parse_page, callback_gitlab

URL_GITLAB = "https://about.gitlab.com/features/"
DEFAULT_STATUS_CODE = 200
DEFAULT_ENCODING = "utf-8"
GITLAB_FILE = "gitlab_features_expected.html"


@pytest.mark.integration_test()
@pytest.mark.parametrize(
        "target_url, expected_outcome",
        [
            (URL_GITLAB, True)
        ]
)
def test_gitalb_api_succesful(target_url, expected_outcome):
    response = requests.get(target_url)
    assert True == bool(response)


def build_response_mock_from_content(
        content,
        encoding=DEFAULT_ENCODING,
        status_code=DEFAULT_STATUS_CODE):
    response = Namespace(
            text=content.decode(encoding),
            content=content,
            encoding=encoding,
            status_code=status_code,
    )
    return response


def open_file():
    with open(GITLAB_FILE, "rb") as content_fin:
        content = content_fin.read()
    return content


@pytest.mark.slow()
def test_parse_page():
    content = open_file()
    page = parse_page(content)
    assert True == bool(page)


@pytest.mark.slow()
@patch("requests.get")
def test_request_web(mock_requests_get):
    content = open_file()
    mock_requests_get.return_value = build_response_mock_from_content(
            content=content,
    )
    response = requests.get(URL_GITLAB)
    assert response.status_code == 200
    assert "gitlab" in response.text


@pytest.mark.integration_test()
def test_assert_http_and_local_file():
    online_products = callback_gitlab("gitlab")
    with patch("requests.get", create=True) as mock_requests_get:
        content = open_file()
        mock_requests_get.return_value = build_response_mock_from_content(
                content=content,
        )
        local_products = callback_gitlab("gitlab")

    assert online_products['free_products'] == local_products['free_products'] and online_products['enterprise_products'] == local_products['enterprise_products'], f"expected free product count is {local_products['free_products']}, while you calculated {online_products['free_products']}; expected enterprise product count is {local_products['enterprise_products']}, while you calculated {online_products['enterprise_products']}"
