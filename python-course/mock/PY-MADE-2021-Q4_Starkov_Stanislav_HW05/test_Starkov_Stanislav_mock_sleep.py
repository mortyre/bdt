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
