from unittest.mock import patch
from sleepy import *


@patch("sleepy.sleep")
def test_sleep_add(mock_sleep_add):
    #from pdb import set_trace; set_trace();
    assert 5 == sleep_add(3, 2)
    mock_sleep_add.assert_called_once

@patch("time.sleep")
def test_sleep_multiply(mock_sleep_multiply):
    #from pdb import set_trace; set_trace();
    assert 6 == sleep_multiply(3, 2)
    mock_sleep_multiply.assert_called_once

@patch("time.sleep")
@patch("sleepy.sleep")
def test_can_mock_all_sleep(mock_sleep_add, mock_sleep_multiply):
    outcome = deepest_sleep_function(1, 2)
    assert 5 == outcome
    mock_sleep_add.assert_called_once_with(3)
    mock_sleep_multiply.assert_called_once_with(5)
