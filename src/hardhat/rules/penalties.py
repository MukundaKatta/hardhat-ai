"""OSHA penalty calculator using official fine schedules.

Penalty amounts reflect OSHA's 2024 penalty schedule as adjusted for inflation.
See: https://www.osha.gov/penalties
"""

from __future__ import annotations

from dataclasses import dataclass

from hardhat.models import OSHAViolation, SeverityLevel


@dataclass
class PenaltyAdjustment:
    """Factors that adjust the base penalty amount."""

    gravity: float = 1.0  # 1.0 = high gravity, 0.6 = moderate, 0.3 = low
    employer_size_factor: float = 1.0  # Reduction for small employers
    good_faith_factor: float = 1.0  # Reduction for demonstrated good faith
    history_factor: float = 1.0  # Increase for prior violations


# OSHA 2024 maximum penalty amounts (adjusted annually for inflation)
PENALTY_MAXIMUMS: dict[SeverityLevel, float] = {
    SeverityLevel.DE_MINIMIS: 0,
    SeverityLevel.OTHER_THAN_SERIOUS: 16131,
    SeverityLevel.SERIOUS: 16131,
    SeverityLevel.WILLFUL: 161323,
    SeverityLevel.REPEAT: 161323,
    SeverityLevel.FAILURE_TO_ABATE: 16131,  # Per day beyond abatement date
}

PENALTY_MINIMUMS: dict[SeverityLevel, float] = {
    SeverityLevel.DE_MINIMIS: 0,
    SeverityLevel.OTHER_THAN_SERIOUS: 0,
    SeverityLevel.SERIOUS: 1036,
    SeverityLevel.WILLFUL: 11524,
    SeverityLevel.REPEAT: 11524,
    SeverityLevel.FAILURE_TO_ABATE: 1036,
}

# Employer size reduction factors (number of employees -> reduction percentage)
SIZE_REDUCTION: dict[str, float] = {
    "1-25": 0.40,     # 60% reduction
    "26-100": 0.60,   # 40% reduction
    "101-250": 0.80,  # 20% reduction
    "251+": 1.00,     # no reduction
}

# Gravity-based penalty factors
GRAVITY_FACTORS: dict[str, float] = {
    "high": 1.0,
    "moderate": 0.6,
    "low": 0.3,
    "minimal": 0.1,
}


class PenaltyCalculator:
    """Calculates OSHA penalties following official fine schedules.

    Considers violation severity, employer size, good faith, and violation
    history when computing penalty amounts.
    """

    def __init__(
        self,
        employer_size: str = "251+",
        good_faith: bool = False,
        prior_violations: int = 0,
    ) -> None:
        """Initialize the calculator.

        Args:
            employer_size: One of '1-25', '26-100', '101-250', '251+'.
            good_faith: Whether employer has demonstrated good faith safety efforts.
            prior_violations: Number of prior OSHA violations in the past 5 years.
        """
        self.employer_size = employer_size
        self.size_factor = SIZE_REDUCTION.get(employer_size, 1.0)
        self.good_faith_reduction = 0.75 if good_faith else 1.0
        self.history_multiplier = min(1.0 + (prior_violations * 0.1), 2.0)

    def calculate_penalty(
        self,
        violation: OSHAViolation,
        gravity: str = "high",
        days_past_abatement: int = 0,
    ) -> float:
        """Calculate the penalty for a single OSHA violation.

        Args:
            violation: The OSHA violation to assess.
            gravity: Gravity level ('high', 'moderate', 'low', 'minimal').
            days_past_abatement: Days past the abatement deadline (for failure to abate).

        Returns:
            Calculated penalty amount in dollars.
        """
        if violation.severity == SeverityLevel.DE_MINIMIS:
            return 0.0

        maximum = PENALTY_MAXIMUMS[violation.severity]
        minimum = PENALTY_MINIMUMS[violation.severity]
        gravity_factor = GRAVITY_FACTORS.get(gravity, 1.0)

        # Base penalty from gravity
        base = maximum * gravity_factor

        # Apply adjustment factors
        adjusted = base * self.size_factor * self.good_faith_reduction * self.history_multiplier

        # Failure to abate: per-day penalty
        if violation.severity == SeverityLevel.FAILURE_TO_ABATE and days_past_abatement > 0:
            daily_penalty = min(adjusted, PENALTY_MAXIMUMS[SeverityLevel.FAILURE_TO_ABATE])
            adjusted = daily_penalty * days_past_abatement

        # Ensure within bounds
        if violation.severity not in (SeverityLevel.FAILURE_TO_ABATE,):
            adjusted = max(minimum, min(adjusted, maximum))

        return round(adjusted, 2)

    def calculate_total_penalties(
        self,
        violations: list[OSHAViolation],
        gravity: str = "high",
    ) -> float:
        """Calculate total penalties for a list of violations."""
        return sum(self.calculate_penalty(v, gravity) for v in violations)

    def get_penalty_breakdown(
        self,
        violations: list[OSHAViolation],
        gravity: str = "high",
    ) -> list[dict[str, object]]:
        """Get a detailed breakdown of penalties by violation.

        Returns:
            List of dicts with standard_id, title, severity, and penalty.
        """
        breakdown: list[dict[str, object]] = []
        for v in violations:
            penalty = self.calculate_penalty(v, gravity)
            breakdown.append(
                {
                    "standard_id": v.standard_id,
                    "title": v.title,
                    "severity": v.severity.value,
                    "penalty": penalty,
                }
            )
        return breakdown

    def estimate_worst_case(self, violations: list[OSHAViolation]) -> float:
        """Estimate worst-case penalties assuming maximum gravity and no reductions."""
        return sum(PENALTY_MAXIMUMS[v.severity] for v in violations)
