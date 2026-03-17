"""Tests for PPE and hazard detectors."""

import torch

from hardhat.detector.compliance import ComplianceChecker
from hardhat.detector.hazard import HazardDetector
from hardhat.detector.ppe import PPEDetector, PPEDetectorCNN
from hardhat.models import HazardDetection, HazardType, PPEDetection, PPEType


class TestPPEDetectorCNN:
    def test_model_output_shape(self):
        model = PPEDetectorCNN()
        model.eval()
        x = torch.randn(1, 3, 224, 224)
        with torch.no_grad():
            out = model(x)
        assert out.shape == (1, 6)

    def test_output_range(self):
        model = PPEDetectorCNN()
        model.eval()
        x = torch.randn(2, 3, 224, 224)
        with torch.no_grad():
            out = model(x)
        assert (out >= 0).all() and (out <= 1).all()


class TestPPEDetector:
    def test_detect_returns_all_types(self):
        detector = PPEDetector()
        image = torch.randn(1, 3, 224, 224)
        detections = detector.detect(image)
        assert len(detections) == 6
        types = {d.ppe_type for d in detections}
        assert types == set(PPEType)

    def test_detect_3d_input(self):
        detector = PPEDetector()
        image = torch.randn(3, 224, 224)
        detections = detector.detect(image)
        assert len(detections) == 6

    def test_compliance_summary(self):
        detector = PPEDetector()
        detections = [
            PPEDetection(ppe_type=PPEType.HARD_HAT, detected=True, confidence=0.9),
            PPEDetection(ppe_type=PPEType.VEST, detected=False, confidence=0.3),
        ]
        summary = detector.get_compliance_summary(detections)
        assert summary["hard_hat"] is True
        assert summary["vest"] is False


class TestHazardDetector:
    def test_detect_returns_all_types(self):
        detector = HazardDetector()
        image = torch.randn(1, 3, 224, 224)
        detections = detector.detect(image)
        assert len(detections) == 4
        types = {d.hazard_type for d in detections}
        assert types == set(HazardType)

    def test_risk_assessment_no_hazards(self):
        detector = HazardDetector()
        detections = [
            HazardDetection(hazard_type=HazardType.UNGUARDED_EDGES, detected=False, confidence=0.1),
        ]
        assert detector.assess_risk_level(detections) == "low"


class TestComplianceChecker:
    def test_missing_ppe_generates_violations(self):
        checker = ComplianceChecker()
        detections = [
            PPEDetection(ppe_type=PPEType.HARD_HAT, detected=False, confidence=0.2),
        ]
        violations = checker.check_ppe_compliance(detections)
        assert len(violations) > 0
        assert any("1926.100" in v.standard_id for v in violations)

    def test_detected_ppe_no_violations(self):
        checker = ComplianceChecker()
        detections = [
            PPEDetection(ppe_type=PPEType.HARD_HAT, detected=True, confidence=0.95),
        ]
        violations = checker.check_ppe_compliance(detections)
        assert len(violations) == 0

    def test_hazard_generates_violations(self):
        checker = ComplianceChecker()
        detections = [
            HazardDetection(hazard_type=HazardType.UNGUARDED_EDGES, detected=True, confidence=0.9),
        ]
        violations = checker.check_hazard_compliance(detections)
        assert len(violations) > 0

    def test_compliance_score_perfect(self):
        checker = ComplianceChecker()
        score = checker.calculate_compliance_score([])
        assert score == 100.0

    def test_full_compliance_check_deduplicates(self):
        checker = ComplianceChecker()
        ppe = [
            PPEDetection(ppe_type=PPEType.HARNESS, detected=False, confidence=0.1),
        ]
        hazards = [
            HazardDetection(hazard_type=HazardType.UNGUARDED_EDGES, detected=True, confidence=0.9),
        ]
        violations = checker.full_compliance_check(ppe, hazards)
        ids = [v.standard_id for v in violations]
        assert len(ids) == len(set(ids)), "Violations should be deduplicated"
