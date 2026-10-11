"""Tests for Windows Wi-Fi collector and SSID hashing."""
import pytest
from collectors.wifi_collector import WiFiCollector

def test_wifi_collector_schema():
    collector = WiFiCollector()
    res = collector.get_wifi_telemetry()
    assert isinstance(res, dict)
    assert "connection_state" in res
    assert "ssid_hash" in res
    assert "adapter_name" in res
    assert "signal_percent" in res

def test_wifi_collector_mock_parsing():
    sample_netsh = """
    Name                   : Wi-Fi
    Description            : Intel(R) Wi-Fi 6 AX203
    State                  : connected
    SSID                   : Campus_WiFi
    AP BSSID               : fe:9d:6d:bd:b0:9c
    Radio type             : 802.11ax
    Channel                : 36
    Receive rate (Mbps)    : 144.0
    Transmit rate (Mbps)   : 144.0
    Signal                 : 95%
    Rssi                   : -45
    """
    collector = WiFiCollector()
    parsed = collector._parse_netsh_output(sample_netsh)
    assert parsed["adapter_name"] == "Wi-Fi"
    assert parsed["connection_state"] == "connected"
    assert parsed["ssid"] == "Campus_WiFi"
    assert parsed["ssid_hash"] is not None
    assert len(parsed["ssid_hash"]) == 12
    assert parsed["channel"] == 36
    assert parsed["signal_percent"] == 95
    assert parsed["rssi_dbm"] == -45
    assert parsed["rx_rate_mbps"] == 144.0
