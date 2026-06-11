import json

from app.dashboard.services.report_export_service import ReportExportService


def test_report_export_service_builds_json():
    service = ReportExportService()
    payload = service.build_json(
        scan={"id": "scan-1", "file_name": "demo.apk"},
        findings=[{"severity": "Alto", "title": "HTTP inseguro"}],
        artifacts=[{"artifact_type": "url", "artifact_value": "http://x.test"}],
    )

    data = json.loads(payload.decode("utf-8"))

    assert data["scan"]["file_name"] == "demo.apk"
    assert data["findings"][0]["severity"] == "Alto"
    assert data["artifacts"][0]["type"] == "url"


def test_report_export_service_builds_csv():
    service = ReportExportService()
    payload = service.build_csv(
        [{"severity": "Medio", "title": "Libreria nativa"}]
    )

    text = payload.decode("utf-8")

    assert "severity" in text
    assert "Libreria nativa" in text
