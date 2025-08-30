import pytest
import os
import json
import tempfile
from unittest.mock import patch, MagicMock
from pipeline.ingest.data_collector import (
    collect_from_file,
    collect_from_syslog,
    collect_from_json_file,
    collect_from_csv_file,
    collect_from_log_file
)


@pytest.fixture
def sample_json_file():
    # Create a temporary JSON file for testing
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w+") as temp_file:
        json.dump([
            {"timestamp": "2023-06-01T12:00:00", "source_ip": "192.168.1.1", "destination_ip": "10.0.0.1", "event_type": "connection"},
            {"timestamp": "2023-06-01T12:05:00", "source_ip": "192.168.1.2", "destination_ip": "10.0.0.2", "event_type": "authentication"}
        ], temp_file)
    
    yield temp_file.name
    
    # Clean up the temporary file
    os.unlink(temp_file.name)


@pytest.fixture
def sample_csv_file():
    # Create a temporary CSV file for testing
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w+") as temp_file:
        temp_file.write("timestamp,source_ip,destination_ip,event_type\n")
        temp_file.write("2023-06-01T12:00:00,192.168.1.1,10.0.0.1,connection\n")
        temp_file.write("2023-06-01T12:05:00,192.168.1.2,10.0.0.2,authentication\n")
    
    yield temp_file.name
    
    # Clean up the temporary file
    os.unlink(temp_file.name)


@pytest.fixture
def sample_log_file():
    # Create a temporary log file for testing
    with tempfile.NamedTemporaryFile(suffix=".log", delete=False, mode="w+") as temp_file:
        temp_file.write("Jun 1 12:00:00 server1 app[123]: Connection from 192.168.1.1 to 10.0.0.1\n")
        temp_file.write("Jun 1 12:05:00 server1 app[124]: Authentication attempt from 192.168.1.2\n")
    
    yield temp_file.name
    
    # Clean up the temporary file
    os.unlink(temp_file.name)


def test_collect_from_json_file(sample_json_file):
    # Test collecting data from a JSON file
    data = collect_from_json_file(sample_json_file)
    
    assert len(data) == 2
    assert data[0]["source_ip"] == "192.168.1.1"
    assert data[1]["event_type"] == "authentication"


def test_collect_from_csv_file(sample_csv_file):
    # Test collecting data from a CSV file
    data = collect_from_csv_file(sample_csv_file)
    
    assert len(data) == 2
    assert data[0]["source_ip"] == "192.168.1.1"
    assert data[1]["event_type"] == "authentication"


def test_collect_from_log_file(sample_log_file):
    # Test collecting data from a log file
    pattern = r"(\w+ \d+ \d+:\d+:\d+) (\S+) (\S+): (.+)"
    data = collect_from_log_file(sample_log_file, pattern)
    
    assert len(data) == 2
    assert "Connection from 192.168.1.1 to 10.0.0.1" in data[0]["message"]
    assert "Authentication attempt from 192.168.1.2" in data[1]["message"]


@patch("pipeline.ingest.data_collector.collect_from_json_file")
def test_collect_from_file_json(mock_collect_json, sample_json_file):
    # Mock the configuration
    config = {"file_path": sample_json_file, "format": "json"}
    mock_collect_json.return_value = [{"test": "data"}]
    
    # Test the collect_from_file function with JSON format
    result = collect_from_file(config)
    
    # Verify the correct helper function was called
    mock_collect_json.assert_called_once_with(sample_json_file)
    assert result == [{"test": "data"}]


@patch("pipeline.ingest.data_collector.collect_from_csv_file")
def test_collect_from_file_csv(mock_collect_csv, sample_csv_file):
    # Mock the configuration
    config = {"file_path": sample_csv_file, "format": "csv"}
    mock_collect_csv.return_value = [{"test": "data"}]
    
    # Test the collect_from_file function with CSV format
    result = collect_from_file(config)
    
    # Verify the correct helper function was called
    mock_collect_csv.assert_called_once_with(sample_csv_file)
    assert result == [{"test": "data"}]


@patch("pipeline.ingest.data_collector.collect_from_log_file")
def test_collect_from_file_log(mock_collect_log, sample_log_file):
    # Mock the configuration
    config = {"file_path": sample_log_file, "format": "log", "pattern": r"test pattern"}
    mock_collect_log.return_value = [{"test": "data"}]
    
    # Test the collect_from_file function with log format
    result = collect_from_file(config)
    
    # Verify the correct helper function was called
    mock_collect_log.assert_called_once_with(sample_log_file, r"test pattern")
    assert result == [{"test": "data"}]


def test_collect_from_file_invalid_format():
    # Test with an invalid format
    config = {"file_path": "test.xyz", "format": "xyz"}
    
    # Should raise a ValueError for unsupported format
    with pytest.raises(ValueError, match="Unsupported file format"):
        collect_from_file(config)


def test_collect_from_file_missing_file():
    # Test with a non-existent file
    config = {"file_path": "nonexistent_file.json", "format": "json"}
    
    # Should raise a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        collect_from_file(config)


@patch("pipeline.ingest.data_collector.collect_from_log_file")
def test_collect_from_syslog(mock_collect_log):
    # Mock the configuration and log file collection
    config = {"syslog_path": "/var/log/syslog", "pattern": r"test pattern"}
    mock_collect_log.return_value = [{"test": "syslog data"}]
    
    # Test the collect_from_syslog function
    result = collect_from_syslog(config)
    
    # Verify collect_from_log_file was called with the correct parameters
    mock_collect_log.assert_called_once_with("/var/log/syslog", r"test pattern")
    assert result == [{"test": "syslog data"}]