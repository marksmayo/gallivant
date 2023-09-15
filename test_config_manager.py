# test_config_loader.py
import pytest
import json
from config_manager import load_config


def test_load_valid_config(mocker):
    mock_file_content = '{"key": "value"}'
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_file_content))
    mocker.patch("json.load", return_value=json.loads(mock_file_content))

    result = load_config()

    assert result == {"key": "value"}


def test_load_corrupted_config(mocker):
    mock_file_content = '{"key": "value" '  # Corrupted JSON
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_file_content))
    mocker.patch(
        "json.load", side_effect=json.JSONDecodeError("Invalid JSON", "doc", 0)
    )

    with pytest.raises(json.JSONDecodeError):
        load_config()


def test_load_config_file_not_found(mocker):
    mocker.patch("builtins.open", side_effect=FileNotFoundError("File not found"))

    with pytest.raises(FileNotFoundError):
        load_config()
