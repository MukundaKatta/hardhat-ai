"""Tests for hardhat-ai pydantic models."""

import pytest
from hardhat.models import (
    HazardDetection,
    HazardType,
    InspectionReport,
    InspectionType,
    OSHAViolation,
    PPEDetection,
    PPEType,
    SafetyFinding,
    SeverityLevel,
)


class TestPPEDetection:
    def test_create_detection(self):
        d = PPEDetection(ppe_type=PPEType.HARD_HAT, detected=True, confidence=0.95)
        assert d.ppe_type == PPEType.HARD_HAT
        assert d.detected is True
        assert d.confidence == 0.95

    def test_confidence_bounds(self):
        with pytest.raises(Exception):
            PPEDetection(ppe_type=PPEType.VEST, detected=True, confidence=1.5)

    def test_bounding_box_optional(self):
        d = PPEDetection(ppe_type=PPEType.GLOVES, detected=False, confidence=0.2)
        assert d.bounding_box is None


class TestHazardDetection:
    def test_create_hazard(self):
        h = HazardDetection(
            hazard_type=HazardType.UNGUARDED_EDGES, detected=True, confidence=0.88
        )
        assert h.hazard_type == HazardType.UNGUARDED_EDGES
        assert h.detected is True

    def test_location_description_default(self):
        h = HazardDetection(
            hazard_type=HazardType.ELECTRICAL_HAZARDS, detected=False, confidence=0.1
        )
        assert h.location_description == ""


class TestOSHAViolation:
    def test_create_violation(self):
        v = OSHAViolation(
            standard_id="1926.100(a)",
            title="Head Protection",
            description="Employees must wear hard hats.",
            severity=SeverityLevel.SERIOUS,
            subpart="E",
            penalty_min=1036,
            penalty_max=15625,
        )
        assert v.standard_id == "1926.100(a)"
        assert v.severity == SeverityLevel.SERIOUS
        assert v.abatement_days == 30


class TestSafetyFinding:
    def test_create_finding(self):
        f = SafetyFinding(
            finding_id="PPE-001",
            category="PPE",
            description="Missing hard hat",
        )
        assert f.finding_id == "PPE-001"
        assert f.violations == []
        assert f.ppe_detections == []

    def test_finding_with_violations(self):
        v = OSHAViolation(
            standard_id="1926.100(a)",
            title="Head Protection",
            description="Hard hat required",
            severity=SeverityLevel.SERIOUS,
        )
        f = SafetyFinding(
            finding_id="PPE-002",
            category="PPE",
            description="Missing hard hat",
            violations=[v],
        )
        assert len(f.violations) == 1


class TestInspectionReport:
    def test_empty_report(self):
        r = InspectionReport(
            report_id="RPT-001",
            site_name="Test Site",
            inspection_type=InspectionType.DAILY,
        )
        assert r.violation_count == 0
        assert r.serious_violations == []
        assert r.passed is True

    def test_report_with_violations(self):
        serious = OSHAViolation(
            standard_id="1926.501(b)(1)",
            title="Fall Protection",
            description="Fall protection required",
            severity=SeverityLevel.SERIOUS,
        )
        minor = OSHAViolation(
            standard_id="1926.200(a)",
            title="Signs",
            description="Signs required",
            severity=SeverityLevel.OTHER_THAN_SERIOUS,
        )
        r = InspectionReport(
            report_id="RPT-002",
            site_name="Test Site",
            inspection_type=InspectionType.WEEKLY,
            violations=[serious, minor],
        )
        assert r.violation_count == 2
        assert len(r.serious_violations) == 1
