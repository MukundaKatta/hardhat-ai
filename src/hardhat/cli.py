"""Command-line interface for Hardhat-AI."""

from __future__ import annotations

import click
from rich.console import Console

from hardhat.models import InspectionType
from hardhat.report import ReportGenerator
from hardhat.simulator import ConstructionSiteSimulator

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="hardhat-ai")
def cli() -> None:
    """Hardhat-AI: Construction Safety Compliance Checker.

    Detect PPE violations, identify site hazards, and map findings
    to real OSHA standards with penalty calculations.
    """


@cli.command()
@click.option("--site", required=True, help="Construction site name.")
@click.option(
    "--type",
    "inspection_type",
    type=click.Choice(["daily", "weekly", "monthly"], case_sensitive=False),
    default="daily",
    help="Inspection type.",
)
@click.option(
    "--scenario",
    type=click.Choice(["well_managed", "average", "poor"], case_sensitive=False),
    default="average",
    help="Site condition scenario for simulation.",
)
@click.option("--workers", default=5, help="Number of workers to check.")
@click.option("--zones", default=4, help="Number of zones to scan.")
@click.option("--seed", default=None, type=int, help="Random seed for reproducibility.")
def inspect(
    site: str,
    inspection_type: str,
    scenario: str,
    workers: int,
    zones: int,
    seed: int | None,
) -> None:
    """Run a simulated safety inspection on a construction site."""
    itype = InspectionType(inspection_type.lower())
    simulator = ConstructionSiteSimulator(scenario=scenario, seed=seed)
    report = simulator.run_inspection(
        site_name=site,
        inspection_type=itype,
        num_workers=workers,
        num_zones=zones,
    )
    generator = ReportGenerator(console=console)
    generator.print_report(report)


@cli.command("check-ppe")
@click.option("--image", default=None, help="Path to site photo (uses simulation if omitted).")
@click.option("--scenario", default="average", help="Simulation scenario.")
@click.option("--seed", default=None, type=int, help="Random seed.")
def check_ppe(image: str | None, scenario: str, seed: int | None) -> None:
    """Check PPE compliance from a site image or simulation."""
    if image is not None:
        console.print("[yellow]Image analysis requires a trained model. Running simulation instead.[/]")

    simulator = ConstructionSiteSimulator(scenario=scenario, seed=seed)
    findings = simulator.simulate_ppe_detections(num_workers=5)

    if not findings:
        console.print("[green]All workers are wearing required PPE.[/]")
        return

    for finding in findings:
        console.print(f"[red]Finding {finding.finding_id}:[/] {finding.description}")
        for v in finding.violations:
            console.print(f"  -> OSHA {v.standard_id}: {v.title}")


@cli.command("scan-hazards")
@click.option("--image", default=None, help="Path to site photo (uses simulation if omitted).")
@click.option("--scenario", default="average", help="Simulation scenario.")
@click.option("--seed", default=None, type=int, help="Random seed.")
def scan_hazards(image: str | None, scenario: str, seed: int | None) -> None:
    """Scan for construction site hazards."""
    if image is not None:
        console.print("[yellow]Image analysis requires a trained model. Running simulation instead.[/]")

    simulator = ConstructionSiteSimulator(scenario=scenario, seed=seed)
    findings = simulator.simulate_hazard_scan(num_zones=6)

    if not findings:
        console.print("[green]No hazards detected in scanned zones.[/]")
        return

    for finding in findings:
        console.print(f"[red]Finding {finding.finding_id}:[/] {finding.description}")
        for v in finding.violations:
            console.print(f"  -> OSHA {v.standard_id}: {v.title}")


@cli.command()
@click.option("--site", required=True, help="Construction site name.")
@click.option("--scenario", default="average", help="Simulation scenario.")
@click.option("--seed", default=None, type=int, help="Random seed.")
def report(site: str, scenario: str, seed: int | None) -> None:
    """Generate a full compliance report for a site."""
    simulator = ConstructionSiteSimulator(scenario=scenario, seed=seed)
    inspection_report = simulator.run_inspection(site_name=site, num_workers=8, num_zones=6)
    generator = ReportGenerator(console=console)
    generator.print_report(inspection_report)


@cli.command("list-standards")
@click.option("--subpart", default=None, help="Filter by subpart letter (e.g., M for Fall Protection).")
@click.option("--search", default=None, help="Search keyword in standard titles/descriptions.")
def list_standards(subpart: str | None, search: str | None) -> None:
    """List OSHA construction standards in the database."""
    from rich.table import Table

    from hardhat.rules.osha import OSHAStandards

    standards_db = OSHAStandards()

    if search:
        standards = standards_db.search(search)
    elif subpart:
        standards = standards_db.list_by_subpart(subpart)
    else:
        standards = standards_db.list_all()

    table = Table(title=f"OSHA Standards ({len(standards)} results)")
    table.add_column("Standard", style="cyan", width=22)
    table.add_column("Title", width=35)
    table.add_column("Subpart", width=8)
    table.add_column("Severity", width=16)

    for s in standards:
        table.add_row(s.standard_id, s.title, s.subpart, s.severity.value)

    console.print(table)


if __name__ == "__main__":
    cli()
