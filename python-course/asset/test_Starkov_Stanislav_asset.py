from asset import *
import logging
import pytest

def test_read_log_files(caplog, capsys):
    caplog.set_level("DEBUG")
    with open("asset.txt") as file:
        print_asset_revenue(file, [1, 3, 5])
    captured = capsys.readouterr()
    #assert 'reading asset file' == captured.out
    #assert 'reading asset file' == captured.err
    assert any('building asset object' in message for message in caplog.messages), (
        "there is no 'building asset object' message in logs"
        )
    assert any("reading asset file" in message for message in caplog.messages), (
        "there is no 'reading asset file' message in logs"
        )
    assert all(record.levelno <= logging.WARNING for record in caplog.records), (
        "there is no WARNING messages"
        )

def test_read_log_files_warning_messages(caplog, capsys):
    caplog.set_level("DEBUG")
    with open("asset.txt") as file:
        print_asset_revenue(file, [1, 3, 5, 6, 7, 8])
    captured = capsys.readouterr()
    assert any("too many periods were provided" in message for message in caplog.messages), (
        "there is no 'too many periods were provided' message in logs"
        )
