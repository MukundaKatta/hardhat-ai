"""Tests for inspection protocols."""

from hardhat.rules.inspection import CheckFrequency, InspectionProtocol


class TestInspectionProtocol:
    def setup_method(self):
        self.protocol = InspectionProtocol()

    def test_daily_checks_exist(self):
        checks = self.protocol.get_checklist(CheckFrequency.DAILY)
        assert len(checks) >= 10

    def test_weekly_checks_exist(self):
        checks = self.protocol.get_checklist(CheckFrequency.WEEKLY)
        assert len(checks) >= 5

    def test_monthly_checks_exist(self):
        checks = self.protocol.get_checklist(CheckFrequency.MONTHLY)
        assert len(checks) >= 5

    def test_critical_daily_checks(self):
        critical = self.protocol.get_critical_checks(CheckFrequency.DAILY)
        assert len(critical) >= 4

    def test_checks_by_category(self):
        ppe_checks = self.protocol.get_checks_by_category("PPE")
        assert len(ppe_checks) >= 2

    def test_total_checks(self):
        assert self.protocol.total_checks >= 25

    def test_checks_have_osha_reference(self):
        for check in self.protocol.get_checklist(CheckFrequency.DAILY):
            assert check.osha_reference.startswith("1926.")
