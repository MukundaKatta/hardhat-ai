"""Tests for penalty calculator."""

from hardhat.models import OSHAViolation, SeverityLevel
from hardhat.rules.penalties import PenaltyCalculator


def _make_violation(severity: SeverityLevel) -> OSHAViolation:
    return OSHAViolation(
        standard_id="1926.100(a)",
        title="Test",
        description="Test violation",
        severity=severity,
    )


class TestPenaltyCalculator:
    def test_de_minimis_no_penalty(self):
        calc = PenaltyCalculator()
        v = _make_violation(SeverityLevel.DE_MINIMIS)
        assert calc.calculate_penalty(v) == 0.0

    def test_serious_has_minimum(self):
        calc = PenaltyCalculator()
        v = _make_violation(SeverityLevel.SERIOUS)
        penalty = calc.calculate_penalty(v, gravity="low")
        assert penalty >= 1036

    def test_willful_high_penalty(self):
        calc = PenaltyCalculator()
        v = _make_violation(SeverityLevel.WILLFUL)
        penalty = calc.calculate_penalty(v, gravity="high")
        assert penalty >= 11524

    def test_small_employer_reduction(self):
        calc_large = PenaltyCalculator(employer_size="251+")
        calc_small = PenaltyCalculator(employer_size="1-25")
        v = _make_violation(SeverityLevel.SERIOUS)
        assert calc_small.calculate_penalty(v) < calc_large.calculate_penalty(v)

    def test_good_faith_reduction(self):
        calc_no = PenaltyCalculator(good_faith=False)
        calc_yes = PenaltyCalculator(good_faith=True)
        v = _make_violation(SeverityLevel.SERIOUS)
        assert calc_yes.calculate_penalty(v) <= calc_no.calculate_penalty(v)

    def test_total_penalties(self):
        calc = PenaltyCalculator()
        violations = [_make_violation(SeverityLevel.SERIOUS) for _ in range(3)]
        total = calc.calculate_total_penalties(violations)
        single = calc.calculate_penalty(violations[0])
        assert total == single * 3

    def test_penalty_breakdown(self):
        calc = PenaltyCalculator()
        violations = [_make_violation(SeverityLevel.SERIOUS)]
        breakdown = calc.get_penalty_breakdown(violations)
        assert len(breakdown) == 1
        assert "penalty" in breakdown[0]
        assert "standard_id" in breakdown[0]

    def test_worst_case(self):
        calc = PenaltyCalculator()
        violations = [_make_violation(SeverityLevel.WILLFUL)]
        worst = calc.estimate_worst_case(violations)
        assert worst == 161323
