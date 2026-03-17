"""Tests for OSHA standards database."""

from hardhat.models import SeverityLevel
from hardhat.rules.osha import OSHAStandards


class TestOSHAStandards:
    def setup_method(self):
        self.standards = OSHAStandards()

    def test_has_30_plus_standards(self):
        assert self.standards.count >= 30

    def test_get_known_standard(self):
        s = self.standards.get_standard("1926.100(a)")
        assert s is not None
        assert s.title == "Head Protection"
        assert s.subpart == "E"

    def test_get_fall_protection_standard(self):
        s = self.standards.get_standard("1926.501(b)(1)")
        assert s is not None
        assert "fall" in s.title.lower() or "fall" in s.description.lower()

    def test_get_scaffold_standard(self):
        s = self.standards.get_standard("1926.451(a)(1)")
        assert s is not None
        assert "scaffold" in s.title.lower()

    def test_get_nonexistent_returns_none(self):
        assert self.standards.get_standard("9999.999") is None

    def test_list_by_subpart(self):
        fall_protection = self.standards.list_by_subpart("M")
        assert len(fall_protection) >= 5
        for s in fall_protection:
            assert s.subpart == "M"

    def test_list_by_severity(self):
        serious = self.standards.list_by_severity(SeverityLevel.SERIOUS)
        assert len(serious) >= 20

    def test_search_by_keyword(self):
        results = self.standards.search("scaffold")
        assert len(results) >= 3

    def test_search_fall(self):
        results = self.standards.search("fall")
        assert len(results) >= 4

    def test_key_standards_exist(self):
        key_ids = [
            "1926.100(a)", "1926.501(b)(1)", "1926.451(a)(1)",
            "1926.404(b)(1)(i)", "1926.502(d)", "1926.652(a)(1)",
        ]
        for std_id in key_ids:
            assert self.standards.get_standard(std_id) is not None, f"Missing standard {std_id}"
