"""Tests for Ping Monitor and dual-path measurement."""
import pytest
from collectors.ping_monitor import PingMonitor

def test_ping_monitor_handles_none_host():
    monitor = PingMonitor()
    res = monitor.ping_target(None)
    assert res["reachable"] is False
    assert res["packet_loss"] == 100.0
    assert res["latency"] is None

def test_ping_monitor_dual_paths_schema():
    monitor = PingMonitor(ping_count=1, timeout_ms=500)
    res = monitor.measure_dual_paths("127.0.0.1")
    assert "gateway_latency" in res
    assert "gateway_packet_loss" in res
    assert "gateway_jitter" in res
    assert "internet_latency" in res
    assert "internet_packet_loss" in res
    assert "internet_jitter" in res
