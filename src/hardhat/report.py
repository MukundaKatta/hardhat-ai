"""Report generation for construction safety inspections."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from hardhat.models import InspectionReport, SeverityLevel


class ReportGenerator:
    """Generates rich-formatted safety inspection reports."""

    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()

    def print_report(self, report: InspectionReport) -> None:
        """Print a full inspection report to the console."""
        self._print_header(report)
        self._print_summary(report)
        self._print_findings(report)
        self._print_violations(report)
        self._print_penalties(report)
        self._print_recommendations(report)
        self._print_footer(report)

    def _print_header(self, report: InspectionReport) -> None:
        status = "[bold green]PASSED[/]" if report.passed else "[bold red]FAILED[/]"
        header = Text.from_markup(
            f"[bold]Construction Safety Inspection Report[/]\n\n"
            f"Report ID:  {report.report_id}\n"
            f"Site:       {report.site_name}\n"
            f"Inspector:  {report.inspector}\n"
            f"Type:       {report.inspection_type.value.title()}\n"
            f"Date:       {report.date.strftime('%Y-%m-%d %H:%M')}\n"
            f"Status:     {status}"
        )
        self.console.print(Panel(header, title="HARDHAT-AI", border_style="blue"))

    def _print_summary(self, report: InspectionReport) -> None:
        score_color = "green" if report.compliance_score >= 80 else "yellow" if report.compliance_score >= 60 else "red"
        table = Table(title="Inspection Summary", show_header=False)
        table.add_column("Metric", style="bold")
        table.add_column("Value")
        table.add_row("Compliance Score", f"[{score_color}]{report.compliance_score:.1f}%[/]")
        table.add_row("Total Findings", str(len(report.findings)))
        table.add_row("OSHA Violations", str(report.violation_count))
        table.add_row("Serious Violations", str(len(report.serious_violations)))
        table.add_row("Estimated Penalties", f"${report.total_penalty:,.2f}")
        self.console.print(table)
        self.console.print()

    def _print_findings(self, report: InspectionReport) -> None:
        if not report.findings:
            self.console.print("[green]No safety findings. Site is compliant.[/]\n")
            return

        table = Table(title="Safety Findings")
        table.add_column("ID", style="cyan", width=16)
        table.add_column("Category", width=18)
        table.add_column("Severity", width=14)
        table.add_column("Description", min_width=40)

        for finding in report.findings:
            severity_style = self._severity_style(finding.severity)
            table.add_row(
                finding.finding_id,
                finding.category,
                f"[{severity_style}]{finding.severity.value}[/]",
                finding.description,
            )
        self.console.print(table)
        self.console.print()

    def _print_violations(self, report: InspectionReport) -> None:
        if not report.violations:
            self.console.print("[green]No OSHA violations identified.[/]\n")
            return

        table = Table(title="OSHA Violations")
        table.add_column("Standard", style="cyan", width=22)
        table.add_column("Title", width=30)
        table.add_column("Severity", width=14)
        table.add_column("Subpart", width=8)
        table.add_column("Penalty Range", width=18)

        for v in report.violations:
            severity_style = self._severity_style(v.severity)
            table.add_row(
                v.standard_id,
                v.title,
                f"[{severity_style}]{v.severity.value}[/]",
                v.subpart,
                f"${v.penalty_min:,.0f} - ${v.penalty_max:,.0f}",
            )
        self.console.print(table)
        self.console.print()

    def _print_penalties(self, report: InspectionReport) -> None:
        if report.total_penalty == 0:
            return
        style = "red" if report.total_penalty > 50000 else "yellow" if report.total_penalty > 10000 else "green"
        self.console.print(
            Panel(
                f"[bold {style}]Total Estimated Penalties: ${report.total_penalty:,.2f}[/]",
                title="Penalty Assessment",
                border_style=style,
            )
        )
        self.console.print()

    def _print_recommendations(self, report: InspectionReport) -> None:
        if not report.recommendations:
            return
        recs = "\n".join(f"  {i+1}. {r}" for i, r in enumerate(report.recommendations))
        self.console.print(Panel(recs, title="Recommendations", border_style="cyan"))
        self.console.print()

    def _print_footer(self, report: InspectionReport) -> None:
        self.console.print(
            "[dim]Report generated by Hardhat-AI. This report is for informational "
            "purposes and does not constitute legal advice. Always consult with a "
            "qualified safety professional for official compliance determinations.[/]"
        )

    @staticmethod
    def _severity_style(severity: SeverityLevel) -> str:
        return {
            SeverityLevel.DE_MINIMIS: "dim",
            SeverityLevel.OTHER_THAN_SERIOUS: "yellow",
            SeverityLevel.SERIOUS: "red",
            SeverityLevel.WILLFUL: "bold red",
            SeverityLevel.REPEAT: "bold red",
            SeverityLevel.FAILURE_TO_ABATE: "bold magenta",
        }.get(severity, "white")
