"""Inspection protocols for construction site safety checks."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class CheckFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class SafetyCheck:
    """A single safety check item within an inspection protocol."""

    check_id: str
    description: str
    category: str
    osha_reference: str
    frequency: CheckFrequency
    critical: bool = False


# Daily safety checks
_DAILY_CHECKS: list[dict] = [
    {
        "check_id": "D-001",
        "description": "Verify all workers are wearing hard hats in designated areas",
        "category": "PPE",
        "osha_reference": "1926.100(a)",
        "frequency": CheckFrequency.DAILY,
        "critical": True,
    },
    {
        "check_id": "D-002",
        "description": "Verify high-visibility vests are worn near vehicle traffic",
        "category": "PPE",
        "osha_reference": "1926.201(a)",
        "frequency": CheckFrequency.DAILY,
        "critical": True,
    },
    {
        "check_id": "D-003",
        "description": "Inspect fall protection harnesses for damage before use",
        "category": "Fall Protection",
        "osha_reference": "1926.502(d)",
        "frequency": CheckFrequency.DAILY,
        "critical": True,
    },
    {
        "check_id": "D-004",
        "description": "Check guardrails on all elevated platforms and floor openings",
        "category": "Fall Protection",
        "osha_reference": "1926.502(b)(1)",
        "frequency": CheckFrequency.DAILY,
        "critical": True,
    },
    {
        "check_id": "D-005",
        "description": "Verify GFCI protection on all temporary electrical outlets",
        "category": "Electrical",
        "osha_reference": "1926.404(b)(1)(i)",
        "frequency": CheckFrequency.DAILY,
        "critical": True,
    },
    {
        "check_id": "D-006",
        "description": "Inspect extension cords and flexible cables for damage",
        "category": "Electrical",
        "osha_reference": "1926.405(a)(2)(ii)(I)",
        "frequency": CheckFrequency.DAILY,
        "critical": False,
    },
    {
        "check_id": "D-007",
        "description": "Ensure adequate housekeeping - clear walkways and work areas",
        "category": "General",
        "osha_reference": "1926.20(b)(1)",
        "frequency": CheckFrequency.DAILY,
        "critical": False,
    },
    {
        "check_id": "D-008",
        "description": "Verify first aid kit is stocked and accessible",
        "category": "Medical",
        "osha_reference": "1926.50(a)",
        "frequency": CheckFrequency.DAILY,
        "critical": False,
    },
    {
        "check_id": "D-009",
        "description": "Check ladder placement angles and top extension",
        "category": "Ladders",
        "osha_reference": "1926.1053(b)(1)",
        "frequency": CheckFrequency.DAILY,
        "critical": True,
    },
    {
        "check_id": "D-010",
        "description": "Ensure potable water supply is available",
        "category": "Sanitation",
        "osha_reference": "1926.51(a)",
        "frequency": CheckFrequency.DAILY,
        "critical": False,
    },
    {
        "check_id": "D-011",
        "description": "Verify all safety signs and barricades are in place",
        "category": "Signs",
        "osha_reference": "1926.200(a)",
        "frequency": CheckFrequency.DAILY,
        "critical": False,
    },
    {
        "check_id": "D-012",
        "description": "Check eye protection availability for grinding/cutting operations",
        "category": "PPE",
        "osha_reference": "1926.102(a)(1)",
        "frequency": CheckFrequency.DAILY,
        "critical": True,
    },
]

# Weekly safety checks
_WEEKLY_CHECKS: list[dict] = [
    {
        "check_id": "W-001",
        "description": "Inspect all scaffolding for structural integrity and proper assembly",
        "category": "Scaffolds",
        "osha_reference": "1926.451(a)(1)",
        "frequency": CheckFrequency.WEEKLY,
        "critical": True,
    },
    {
        "check_id": "W-002",
        "description": "Verify scaffold platforms are fully planked and minimum 18 inches wide",
        "category": "Scaffolds",
        "osha_reference": "1926.451(b)(1)",
        "frequency": CheckFrequency.WEEKLY,
        "critical": True,
    },
    {
        "check_id": "W-003",
        "description": "Inspect scaffold guardrails on platforms above 10 feet",
        "category": "Scaffolds",
        "osha_reference": "1926.451(g)(1)",
        "frequency": CheckFrequency.WEEKLY,
        "critical": True,
    },
    {
        "check_id": "W-004",
        "description": "Review excavation protective systems (shoring, sloping, shields)",
        "category": "Excavations",
        "osha_reference": "1926.652(a)(1)",
        "frequency": CheckFrequency.WEEKLY,
        "critical": True,
    },
    {
        "check_id": "W-005",
        "description": "Inspect fire extinguishers for charge and accessibility",
        "category": "Fire Protection",
        "osha_reference": "1926.150(a)",
        "frequency": CheckFrequency.WEEKLY,
        "critical": False,
    },
    {
        "check_id": "W-006",
        "description": "Check flammable liquid storage containers for proper labeling and condition",
        "category": "Fire Protection",
        "osha_reference": "1926.152(a)(1)",
        "frequency": CheckFrequency.WEEKLY,
        "critical": False,
    },
    {
        "check_id": "W-007",
        "description": "Inspect stairway access points at elevation changes of 19 inches or more",
        "category": "Stairways",
        "osha_reference": "1926.1050(a)",
        "frequency": CheckFrequency.WEEKLY,
        "critical": False,
    },
    {
        "check_id": "W-008",
        "description": "Verify steel erection fall protection above 15 feet",
        "category": "Steel Erection",
        "osha_reference": "1926.760(a)",
        "frequency": CheckFrequency.WEEKLY,
        "critical": True,
    },
]

# Monthly safety checks
_MONTHLY_CHECKS: list[dict] = [
    {
        "check_id": "M-001",
        "description": "Review and update the site-specific safety program",
        "category": "Program",
        "osha_reference": "1926.20(b)(1)",
        "frequency": CheckFrequency.MONTHLY,
        "critical": False,
    },
    {
        "check_id": "M-002",
        "description": "Conduct safety training refresher for all employees",
        "category": "Training",
        "osha_reference": "1926.21(b)(2)",
        "frequency": CheckFrequency.MONTHLY,
        "critical": False,
    },
    {
        "check_id": "M-003",
        "description": "Review fall protection training records and update as needed",
        "category": "Training",
        "osha_reference": "1926.503(a)(1)",
        "frequency": CheckFrequency.MONTHLY,
        "critical": False,
    },
    {
        "check_id": "M-004",
        "description": "Verify scaffold training records for all scaffold workers",
        "category": "Training",
        "osha_reference": "1926.454(a)",
        "frequency": CheckFrequency.MONTHLY,
        "critical": False,
    },
    {
        "check_id": "M-005",
        "description": "Conduct noise level monitoring in high-noise areas",
        "category": "Health",
        "osha_reference": "1926.52(b)",
        "frequency": CheckFrequency.MONTHLY,
        "critical": False,
    },
    {
        "check_id": "M-006",
        "description": "Inspect and test all safety nets and anchorage points",
        "category": "Fall Protection",
        "osha_reference": "1926.502(d)",
        "frequency": CheckFrequency.MONTHLY,
        "critical": True,
    },
    {
        "check_id": "M-007",
        "description": "Review accident/incident log and update prevention programs",
        "category": "Program",
        "osha_reference": "1926.20(b)(2)",
        "frequency": CheckFrequency.MONTHLY,
        "critical": False,
    },
    {
        "check_id": "M-008",
        "description": "Verify underground utility location records before new excavation phases",
        "category": "Excavations",
        "osha_reference": "1926.651(a)",
        "frequency": CheckFrequency.MONTHLY,
        "critical": True,
    },
]


@dataclass
class InspectionProtocol:
    """Manages inspection checklists for daily, weekly, and monthly safety checks.

    Provides structured checklists based on real OSHA standards and tracks
    completion of safety inspections.
    """

    daily_checks: list[SafetyCheck] = field(default_factory=list)
    weekly_checks: list[SafetyCheck] = field(default_factory=list)
    monthly_checks: list[SafetyCheck] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.daily_checks:
            self.daily_checks = [SafetyCheck(**c) for c in _DAILY_CHECKS]
        if not self.weekly_checks:
            self.weekly_checks = [SafetyCheck(**c) for c in _WEEKLY_CHECKS]
        if not self.monthly_checks:
            self.monthly_checks = [SafetyCheck(**c) for c in _MONTHLY_CHECKS]

    def get_checklist(self, frequency: CheckFrequency) -> list[SafetyCheck]:
        """Return the checklist for a given inspection frequency."""
        mapping = {
            CheckFrequency.DAILY: self.daily_checks,
            CheckFrequency.WEEKLY: self.weekly_checks,
            CheckFrequency.MONTHLY: self.monthly_checks,
        }
        return mapping[frequency]

    def get_critical_checks(self, frequency: CheckFrequency) -> list[SafetyCheck]:
        """Return only critical checks for a given frequency."""
        return [c for c in self.get_checklist(frequency) if c.critical]

    def get_checks_by_category(self, category: str) -> list[SafetyCheck]:
        """Return all checks across frequencies for a specific category."""
        all_checks = self.daily_checks + self.weekly_checks + self.monthly_checks
        return [c for c in all_checks if c.category.lower() == category.lower()]

    @property
    def total_checks(self) -> int:
        return len(self.daily_checks) + len(self.weekly_checks) + len(self.monthly_checks)
