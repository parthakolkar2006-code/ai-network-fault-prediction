"""Tests for dynamic gateway detection without hardcoded IPs."""
import pytest
from collectors.gateway_detector import GatewayDetector

def test_gateway_detector_runs_without_error():
    detector = GatewayDetector()
    result = detector.get_default_gateway()
    assert isinstance(result, dict)
    assert "gateway_ip" in result
    assert "local_ip" in result
    assert "has_changed" in result

def test_gateway_detector_detects_changes():
    detector = GatewayDetector()
    detector.last_gateway = "99.99.99.99"
    result = detector.get_default_gateway()
    # Should flag change if current gateway is not 99.99.99.99
    if result["gateway_ip"] != "99.99.99.99":
        assert result["has_changed"] is True
