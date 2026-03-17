"""Construction site safety simulator for testing and demonstration."""

from __future__ import annotations

import random
import uuid
from datetime import datetime

import torch

from hardhat.detector.compliance import ComplianceChecker
from hardhat.detector.hazard import HazardDetector
from hardhat.detector.ppe import PPEDetector
from hardhat.models import (
    HazardType,
    InspectionReport,
    InspectionType,
    PPEType,
    SafetyFinding,
    SeverityLevel,
)
from hardhat.rules.penalties import PenaltyCalculator


class ConstructionSiteSimulator:
    """Simulates construction site conditions for safety analysis.

    Generates synthetic detection results, runs compliance checks, and
    produces inspection reports without requiring real image data.
    """

    # Realistic PPE compliance rates by scenario
    SCENARIOS: dict[str, dict[str, float]] = {
        "well_managed": {
            PPEType.HARD_HAT.value: 0.95,
            PPEType.VEST.value: 0.92,
            PPEType.GOGGLES.value: 0.88,
            PPEType.GLOVES.value: 0.85,
            PPEType.BOOTS.value: 0.93,
            PPEType.HARNESS.value: 0.90,
        },
        "average": {
            PPEType.HARD_HAT.value: 0.80,
            PPEType.VEST.value: 0.75,
            PPEType.GOGGLES.value: 0.60,
            PPEType.GLOVES.value: 0.65,
            PPEType.BOOTS.value: 0.78,
            PPEType.HARNESS.value: 0.55,
        },
        "poor": {
            PPEType.HARD_HAT.value: 0.50,
            PPEType.VEST.value: 0.40,
            PPEType.GOGGLES.value: 0.30,
            PPEType.GLOVES.value: 0.35,
            PPEType.BOOTS.value: 0.55,
            PPEType.HARNESS.value: 0.25,
        },
    }

    HAZARD_RATES: dict[str, dict[str, float]] = {
        "well_managed": {
            HazardType.UNGUARDED_EDGES.value: 0.05,
            HazardType.MISSING_GUARDRAILS.value: 0.08,
            HazardType.IMPROPER_SCAFFOLDING.value: 0.03,
            HazardType.ELECTRICAL_HAZARDS.value: 0.04,
        },
        "average": {
            HazardType.UNGUARDED_EDGES.value: 0.20,
            HazardType.MISSING_GUARDRAILS.value: 0.25,
            HazardType.IMPROPER_SCAFFOLDING.value: 0.15,
            HazardType.ELECTRICAL_HAZARDS.value: 0.18,
        },
        "poor": {
            HazardType.UNGUARDED_EDGES.value: 0.55,
            HazardType.MISSING_GUARDRAILS.value: 0.60,
            HazardType.IMPROPER_SCAFFOLDING.value: 0.45,
            HazardType.ELECTRICAL_HAZARDS.value: 0.50,
        },
    }

    def __init__(self, scenario: str = "average", seed: int | None = None) -> None:
        if scenario not in self.SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario}. Use: {list(self.SCENARIOS)}")
        self.scenario = scenario
        self.rng = random.Random(seed)
        self.ppe_detector = PPEDetector()
        self.hazard_detector = HazardDetector()
        self.compliance_checker = ComplianceChecker()

    def generate_synthetic_image(self) -> torch.Tensor:
        """Generate a random synthetic image tensor for simulation."""
        return torch.randn(1, 3, 224, 224)

    def simulate_ppe_detections(self, num_workers: int = 5) -> list[SafetyFinding]:
        """Simulate PPE compliance checks for a number of workers."""
        findings: list[SafetyFinding] = []
        ppe_rates = self.SCENARIOS[self.scenario]

        for i in range(num_workers):
            ppe_detections = []
            for ppe_type in PPEType:
                compliance_rate = ppe_rates.get(ppe_type.value, 0.5)
                detected = self.rng.random() < compliance_rate
                confidence = self.rng.uniform(0.7, 0.99) if detected else self.rng.uniform(0.1, 0.4)
                from hardhat.models import PPEDetection

                ppe_detections.append(
                    PPEDetection(
                        ppe_type=ppe_type,
                        detected=detected,
                        confidence=round(confidence, 4),
                    )
                )

            violations = self.compliance_checker.check_ppe_compliance(ppe_detections)
            missing = [d for d in ppe_detections if not d.detected]

            if missing:
                severity = SeverityLevel.SERIOUS if len(missing) >= 2 else SeverityLevel.OTHER_THAN_SERIOUS
                finding = SafetyFinding(
                    finding_id=f"PPE-{uuid.uuid4().hex[:8]}",
                    category="PPE Compliance",
                    description=f"Worker {i + 1}: Missing {', '.join(d.ppe_type.value for d in missing)}",
                    ppe_detections=ppe_detections,
                    violations=violations,
                    severity=severity,
                    corrective_action="Provide missing PPE immediately and retrain worker on PPE requirements.",
                )
                findings.append(finding)

        return findings

    def simulate_hazard_scan(self, num_zones: int = 4) -> list[SafetyFinding]:
        """Simulate hazard scanning across construction zones."""
        findings: list[SafetyFinding] = []
        hazard_rates = self.HAZARD_RATES[self.scenario]

        zone_names = [
            "Foundation Area", "Framing Zone", "Rooftop Level",
            "Electrical Room", "Excavation Site", "Storage Area",
            "Loading Dock", "Scaffolding Area",
        ]

        for i in range(min(num_zones, len(zone_names))):
            hazard_detections = []
            for hazard_type in HazardType:
                rate = hazard_rates.get(hazard_type.value, 0.2)
                detected = self.rng.random() < rate
                confidence = self.rng.uniform(0.6, 0.95) if detected else self.rng.uniform(0.05, 0.3)
                from hardhat.models import HazardDetection

                hazard_detections.append(
                    HazardDetection(
                        hazard_type=hazard_type,
                        detected=detected,
                        confidence=round(confidence, 4),
                    )
                )

            violations = self.compliance_checker.check_hazard_compliance(hazard_detections)
            detected_hazards = [d for d in hazard_detections if d.detected]

            if detected_hazards:
                finding = SafetyFinding(
                    finding_id=f"HAZ-{uuid.uuid4().hex[:8]}",
                    category="Site Hazard",
                    description=(
                        f"{zone_names[i]}: Detected {', '.join(d.hazard_type.value for d in detected_hazards)}"
                    ),
                    hazard_detections=hazard_detections,
                    violations=violations,
                    severity=SeverityLevel.SERIOUS if len(detected_hazards) >= 2 else SeverityLevel.OTHER_THAN_SERIOUS,
                    corrective_action="Correct identified hazards immediately. Restrict access until resolved.",
                )
                findings.append(finding)

        return findings

    def run_inspection(
        self,
        site_name: str,
        inspection_type: InspectionType = InspectionType.DAILY,
        num_workers: int = 5,
        num_zones: int = 4,
    ) -> InspectionReport:
        """Run a complete simulated inspection.

        Returns:
            A fully populated InspectionReport.
        """
        ppe_findings = self.simulate_ppe_detections(num_workers)
        hazard_findings = self.simulate_hazard_scan(num_zones)
        all_findings = ppe_findings + hazard_findings

        all_violations: list = []
        seen_ids: set[str] = set()
        for finding in all_findings:
            for v in finding.violations:
                if v.standard_id not in seen_ids:
                    seen_ids.add(v.standard_id)
                    all_violations.append(v)

        calculator = PenaltyCalculator()
        total_penalty = calculator.calculate_total_penalties(all_violations)
        compliance_score = self.compliance_checker.calculate_compliance_score(all_violations)

        recommendations = self._generate_recommendations(all_findings)

        return InspectionReport(
            report_id=f"RPT-{uuid.uuid4().hex[:8]}",
            site_name=site_name,
            inspection_type=inspection_type,
            date=datetime.now(),
            findings=all_findings,
            violations=all_violations,
            total_penalty=total_penalty,
            compliance_score=compliance_score,
            recommendations=recommendations,
            passed=compliance_score >= 70.0,
        )

    def _generate_recommendations(self, findings: list[SafetyFinding]) -> list[str]:
        """Generate actionable recommendations based on findings."""
        recommendations: list[str] = []
        has_ppe_issues = any(f.category == "PPE Compliance" for f in findings)
        has_hazards = any(f.category == "Site Hazard" for f in findings)

        if has_ppe_issues:
            recommendations.append("Conduct immediate PPE compliance briefing for all site workers.")
            recommendations.append("Station a competent person at site entrance to verify PPE before entry.")

        if has_hazards:
            recommendations.append("Assign competent person to inspect and correct all identified hazards.")
            recommendations.append("Restrict access to hazardous areas until corrective actions are verified.")

        if not findings:
            recommendations.append("Continue current safety practices. Schedule next routine inspection.")

        recommendations.append("Document all corrective actions taken and maintain records per OSHA requirements.")
        return recommendations
