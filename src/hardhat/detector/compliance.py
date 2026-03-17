"""Compliance checker mapping detections to OSHA violations."""

from __future__ import annotations

from hardhat.models import (
    HazardDetection,
    HazardType,
    OSHAViolation,
    PPEDetection,
    PPEType,
    SeverityLevel,
)
from hardhat.rules.osha import OSHAStandards


# Mapping from missing PPE to OSHA standard IDs
PPE_TO_OSHA: dict[PPEType, list[str]] = {
    PPEType.HARD_HAT: ["1926.100(a)", "1926.100(b)"],
    PPEType.VEST: ["1926.201(a)"],
    PPEType.GOGGLES: ["1926.102(a)(1)", "1926.102(a)(2)"],
    PPEType.GLOVES: ["1926.95(a)"],
    PPEType.BOOTS: ["1926.96(a)"],
    PPEType.HARNESS: ["1926.502(d)", "1926.501(b)(1)"],
}

# Mapping from hazard types to OSHA standard IDs
HAZARD_TO_OSHA: dict[HazardType, list[str]] = {
    HazardType.UNGUARDED_EDGES: ["1926.501(b)(1)", "1926.501(b)(10)", "1926.502(b)(1)"],
    HazardType.MISSING_GUARDRAILS: [
        "1926.502(b)(1)",
        "1926.502(b)(3)",
        "1926.502(b)(4)",
        "1926.1053(a)(4)",
    ],
    HazardType.IMPROPER_SCAFFOLDING: [
        "1926.451(a)(1)",
        "1926.451(b)(1)",
        "1926.451(g)(1)",
        "1926.454(a)",
    ],
    HazardType.ELECTRICAL_HAZARDS: [
        "1926.405(a)(2)(ii)(I)",
        "1926.404(b)(1)(i)",
        "1926.416(a)(1)",
    ],
}


class ComplianceChecker:
    """Maps PPE and hazard detections to OSHA violations."""

    def __init__(self) -> None:
        self.standards = OSHAStandards()

    def check_ppe_compliance(self, detections: list[PPEDetection]) -> list[OSHAViolation]:
        """Check PPE detections against OSHA requirements.

        Args:
            detections: PPE detection results from PPEDetector.

        Returns:
            List of OSHA violations for missing PPE.
        """
        violations: list[OSHAViolation] = []
        for detection in detections:
            if detection.detected:
                continue
            standard_ids = PPE_TO_OSHA.get(detection.ppe_type, [])
            for std_id in standard_ids:
                standard = self.standards.get_standard(std_id)
                if standard is not None:
                    violations.append(standard)
        return violations

    def check_hazard_compliance(self, detections: list[HazardDetection]) -> list[OSHAViolation]:
        """Check hazard detections against OSHA requirements.

        Args:
            detections: Hazard detection results from HazardDetector.

        Returns:
            List of OSHA violations for detected hazards.
        """
        violations: list[OSHAViolation] = []
        for detection in detections:
            if not detection.detected:
                continue
            standard_ids = HAZARD_TO_OSHA.get(detection.hazard_type, [])
            for std_id in standard_ids:
                standard = self.standards.get_standard(std_id)
                if standard is not None:
                    violations.append(standard)
        return violations

    def full_compliance_check(
        self,
        ppe_detections: list[PPEDetection],
        hazard_detections: list[HazardDetection],
    ) -> list[OSHAViolation]:
        """Run a complete compliance check combining PPE and hazard findings.

        Returns:
            Combined, deduplicated list of OSHA violations.
        """
        ppe_violations = self.check_ppe_compliance(ppe_detections)
        hazard_violations = self.check_hazard_compliance(hazard_detections)

        seen: set[str] = set()
        unique: list[OSHAViolation] = []
        for v in ppe_violations + hazard_violations:
            if v.standard_id not in seen:
                seen.add(v.standard_id)
                unique.append(v)
        return unique

    def calculate_compliance_score(self, violations: list[OSHAViolation]) -> float:
        """Calculate a 0-100 compliance score.

        The score decreases based on the number and severity of violations.
        """
        if not violations:
            return 100.0

        penalty_points = 0.0
        for v in violations:
            if v.severity == SeverityLevel.DE_MINIMIS:
                penalty_points += 1
            elif v.severity == SeverityLevel.OTHER_THAN_SERIOUS:
                penalty_points += 3
            elif v.severity == SeverityLevel.SERIOUS:
                penalty_points += 8
            elif v.severity == SeverityLevel.WILLFUL:
                penalty_points += 20
            elif v.severity == SeverityLevel.REPEAT:
                penalty_points += 15
            elif v.severity == SeverityLevel.FAILURE_TO_ABATE:
                penalty_points += 12

        score = max(0.0, 100.0 - penalty_points)
        return round(score, 1)
