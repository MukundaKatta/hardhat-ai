"""Pydantic models for construction safety findings and reports."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class PPEType(str, Enum):
    """Types of Personal Protective Equipment."""

    HARD_HAT = "hard_hat"
    VEST = "vest"
    GOGGLES = "goggles"
    GLOVES = "gloves"
    BOOTS = "boots"
    HARNESS = "harness"


class HazardType(str, Enum):
    """Types of construction site hazards."""

    UNGUARDED_EDGES = "unguarded_edges"
    MISSING_GUARDRAILS = "missing_guardrails"
    IMPROPER_SCAFFOLDING = "improper_scaffolding"
    ELECTRICAL_HAZARDS = "electrical_hazards"


class SeverityLevel(str, Enum):
    """OSHA violation severity levels."""

    DE_MINIMIS = "de_minimis"
    OTHER_THAN_SERIOUS = "other_than_serious"
    SERIOUS = "serious"
    WILLFUL = "willful"
    REPEAT = "repeat"
    FAILURE_TO_ABATE = "failure_to_abate"


class InspectionType(str, Enum):
    """Types of safety inspections."""

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class PPEDetection(BaseModel):
    """A single PPE detection result."""

    ppe_type: PPEType
    detected: bool
    confidence: float = Field(ge=0.0, le=1.0)
    bounding_box: Optional[tuple[int, int, int, int]] = None


class HazardDetection(BaseModel):
    """A single hazard detection result."""

    hazard_type: HazardType
    detected: bool
    confidence: float = Field(ge=0.0, le=1.0)
    location_description: str = ""
    bounding_box: Optional[tuple[int, int, int, int]] = None


class OSHAViolation(BaseModel):
    """An OSHA regulation violation."""

    standard_id: str = Field(description="e.g. 1926.100(a)")
    title: str
    description: str
    severity: SeverityLevel
    subpart: str = ""
    penalty_min: float = 0.0
    penalty_max: float = 0.0
    abatement_days: int = 30


class SafetyFinding(BaseModel):
    """A safety finding from an inspection or detection."""

    finding_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    category: str
    description: str
    ppe_detections: list[PPEDetection] = Field(default_factory=list)
    hazard_detections: list[HazardDetection] = Field(default_factory=list)
    violations: list[OSHAViolation] = Field(default_factory=list)
    severity: SeverityLevel = SeverityLevel.OTHER_THAN_SERIOUS
    corrective_action: str = ""
    photo_reference: Optional[str] = None


class InspectionReport(BaseModel):
    """A complete inspection report."""

    report_id: str
    site_name: str
    inspector: str = "Hardhat-AI"
    inspection_type: InspectionType
    date: datetime = Field(default_factory=datetime.now)
    findings: list[SafetyFinding] = Field(default_factory=list)
    violations: list[OSHAViolation] = Field(default_factory=list)
    total_penalty: float = 0.0
    compliance_score: float = Field(default=100.0, ge=0.0, le=100.0)
    recommendations: list[str] = Field(default_factory=list)
    passed: bool = True

    @property
    def violation_count(self) -> int:
        return len(self.violations)

    @property
    def serious_violations(self) -> list[OSHAViolation]:
        return [
            v
            for v in self.violations
            if v.severity in (SeverityLevel.SERIOUS, SeverityLevel.WILLFUL, SeverityLevel.REPEAT)
        ]
