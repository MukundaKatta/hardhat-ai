"""Tests for the construction site simulator."""

from hardhat.models import InspectionType
from hardhat.simulator import ConstructionSiteSimulator


class TestSimulator:
    def test_well_managed_site(self):
        sim = ConstructionSiteSimulator(scenario="well_managed", seed=42)
        report = sim.run_inspection("Test Site", InspectionType.DAILY)
        assert report.site_name == "Test Site"
        assert report.compliance_score >= 0

    def test_poor_site_has_violations(self):
        sim = ConstructionSiteSimulator(scenario="poor", seed=42)
        report = sim.run_inspection("Bad Site", InspectionType.DAILY, num_workers=10, num_zones=6)
        assert report.violation_count > 0

    def test_reproducible_with_seed(self):
        sim1 = ConstructionSiteSimulator(scenario="average", seed=123)
        sim2 = ConstructionSiteSimulator(scenario="average", seed=123)
        r1 = sim1.run_inspection("Site A")
        r2 = sim2.run_inspection("Site A")
        assert r1.violation_count == r2.violation_count
        assert r1.compliance_score == r2.compliance_score

    def test_invalid_scenario_raises(self):
        import pytest
        with pytest.raises(ValueError):
            ConstructionSiteSimulator(scenario="nonexistent")

    def test_ppe_findings(self):
        sim = ConstructionSiteSimulator(scenario="poor", seed=1)
        findings = sim.simulate_ppe_detections(num_workers=10)
        assert len(findings) > 0

    def test_hazard_findings(self):
        sim = ConstructionSiteSimulator(scenario="poor", seed=1)
        findings = sim.simulate_hazard_scan(num_zones=6)
        assert len(findings) > 0
