"""
Comprehensive Unit & Integration Test for SentinelSOC Backend
"""
import os
import sys

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from fastapi.testclient import TestClient
from app.main import app
from app.core.init_db import init_db

def test_all():
    # Initialize DB tables and seed data
    init_db()

    with TestClient(app) as client:
        # 1. Health check
        res = client.get("/health")
        assert res.status_code == 200, f"Health check failed: {res.text}"
        print("[PASS] Health check passed:", res.json())

        # 2. Get Rules
        res = client.get("/api/v1/rules")
        assert res.status_code == 200
        rules_data = res.json()
        assert rules_data["total"] >= 10
        print(f"[PASS] Detection rules loaded: {rules_data['total']} rules active.")

        # 3. Threat Intel lookup
        res = client.get("/api/v1/threat-intel/lookup?indicator=185.220.101.5")
        assert res.status_code == 200
        ti_data = res.json()
        assert ti_data["threat_level"] in ["HIGH", "CRITICAL"]
        print(f"[PASS] Threat Intel lookup passed: 185.220.101.5 -> {ti_data['threat_level']} (VT: {ti_data['virustotal']['detection_ratio']})")

        # 4. CyberChef Decode test
        res = client.post("/api/v1/tools/cyberchef", json={
            "operation": "base64_decode",
            "input_text": "SGVsbG8gV29ybGQ="
        })
        assert res.status_code == 200
        assert res.json()["output_text"] == "Hello World"
        print("[PASS] CyberChef base64 decode passed: SGVsbG8gV29ybGQ= -> 'Hello World'")

        # 5. Extract IOCs test
        res = client.post("/api/v1/tools/extract-iocs", json={
            "raw_text": "Attacker at 194.26.29.112 downloaded payload from http://bad-site.org/malware.exe with hash 24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c"
        })
        assert res.status_code == 200
        extracted = res.json()
        assert "194.26.29.112" in extracted["ipv4_addresses"]
        assert "24d004a104d4d54034dbcffc2a4b19a11f39008a575aa614ea04703480b1022c" in extracted["sha256_hashes"]
        print("[PASS] IOC regex extractor passed: found IP and SHA256 hash.")

        # 6. Run Simulator Lab 1 (SSH Brute Force)
        res = client.post("/api/v1/simulator/run", json={"scenario_id": "brute_force"})
        assert res.status_code == 200
        sim_data = res.json()
        assert sim_data["logs_generated"] > 0
        assert sim_data["alerts_triggered"] > 0
        print(f"[PASS] Simulator Lab 1 passed: Generated {sim_data['logs_generated']} logs, Triggered {sim_data['alerts_triggered']} alerts.")

        # 7. Check Alerts
        res = client.get("/api/v1/alerts")
        assert res.status_code == 200
        alerts_data = res.json()
        assert alerts_data["total"] > 0
        first_alert_id = alerts_data["alerts"][0]["id"]
        print(f"[PASS] Alerts retrieved: {alerts_data['total']} total alerts in SIEM.")

        # 8. Escalate Alert to Incident
        res = client.post(f"/api/v1/alerts/{first_alert_id}/escalate", json={
            "assigned_to": "soc_analyst",
            "initial_notes": "Triaged and verified malicious source IP in AbuseIPDB."
        })
        assert res.status_code == 201
        incident_data = res.json()
        inc_id = incident_data["id"]
        print(f"[PASS] Escalated Alert #{first_alert_id} to Incident {incident_data['incident_number']}")

        # 9. Generate Incident Report
        res = client.get(f"/api/v1/incidents/{inc_id}/report")
        assert res.status_code == 200
        report_data = res.json()
        assert "SentinelSOC Incident Response Report" in report_data["markdown_report"]
        print(f"[PASS] Incident report generated successfully for {report_data['incident_number']}.")

        # 10. Metrics check
        res = client.get("/api/v1/metrics")
        assert res.status_code == 200
        metrics = res.json()
        print(f"[PASS] Executive Metrics: Threat Level={metrics['threat_level']}, Threat Index={metrics['threat_index_score']}, Open Incidents={metrics['open_incidents']}")

    print("\n==========================================")
    print(" ALL 10 BACKEND TESTS PASSED SUCCESSFULLY! ")
    print("==========================================")

if __name__ == "__main__":
    test_all()
