"""OSHA construction standards database (29 CFR 1926).

Contains 30+ real OSHA construction safety standards with their descriptions,
applicable subparts, severity classifications, and penalty ranges.
"""

from __future__ import annotations

from typing import Optional

from hardhat.models import OSHAViolation, SeverityLevel


# Real OSHA 29 CFR 1926 construction standards
_STANDARDS: list[dict] = [
    # Subpart C - General Safety and Health Provisions
    {
        "standard_id": "1926.20(b)(1)",
        "title": "Accident Prevention Programs",
        "description": (
            "Programs shall provide for frequent and regular inspections of the job "
            "sites, materials, and equipment by competent persons."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "C",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 30,
    },
    {
        "standard_id": "1926.20(b)(2)",
        "title": "Accident Prevention - Unsafe Conditions",
        "description": (
            "The employer shall instruct each employee in the recognition and avoidance "
            "of unsafe conditions and regulations applicable to the work environment."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "C",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 30,
    },
    {
        "standard_id": "1926.21(b)(2)",
        "title": "Safety Training and Education",
        "description": (
            "The employer shall instruct each employee in the recognition and avoidance "
            "of unsafe conditions and the regulations applicable to his work environment."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "C",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 15,
    },
    # Subpart D - Occupational Health and Environmental Controls
    {
        "standard_id": "1926.50(a)",
        "title": "Medical Services and First Aid",
        "description": (
            "The employer shall ensure the availability of medical personnel for advice "
            "and consultation on matters of occupational health."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "D",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 15,
    },
    {
        "standard_id": "1926.51(a)",
        "title": "Sanitation - Potable Water",
        "description": "An adequate supply of potable water shall be provided in all places of employment.",
        "severity": SeverityLevel.OTHER_THAN_SERIOUS,
        "subpart": "D",
        "penalty_min": 0,
        "penalty_max": 15625,
        "abatement_days": 7,
    },
    {
        "standard_id": "1926.52(b)",
        "title": "Occupational Noise Exposure",
        "description": (
            "When employees are subjected to sound exceeding those listed in Table D-2, "
            "feasible administrative or engineering controls shall be utilized."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "D",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 30,
    },
    # Subpart E - Personal Protective and Life Saving Equipment
    {
        "standard_id": "1926.95(a)",
        "title": "PPE - General Requirements",
        "description": (
            "Protective equipment, including personal protective equipment for eyes, face, "
            "head, and extremities, shall be provided, used, and maintained."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "E",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 7,
    },
    {
        "standard_id": "1926.96(a)",
        "title": "Occupational Foot Protection",
        "description": (
            "Safety-toe footwear shall be worn by employees to protect against foot injuries "
            "due to falling or rolling objects, objects piercing the sole, or electrical hazards."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "E",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 7,
    },
    {
        "standard_id": "1926.100(a)",
        "title": "Head Protection",
        "description": (
            "Employees working in areas where there is a possible danger of head injury from "
            "impact, or from falling or flying objects, shall be protected by protective helmets."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "E",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 1,
    },
    {
        "standard_id": "1926.100(b)",
        "title": "Head Protection - Specifications",
        "description": (
            "Helmets for the protection of employees against impact and penetration of "
            "falling and flying objects shall meet ANSI Z89.1-2014 specifications."
        ),
        "severity": SeverityLevel.OTHER_THAN_SERIOUS,
        "subpart": "E",
        "penalty_min": 0,
        "penalty_max": 15625,
        "abatement_days": 7,
    },
    {
        "standard_id": "1926.102(a)(1)",
        "title": "Eye and Face Protection",
        "description": (
            "Employees shall be provided with eye and face protection equipment when "
            "machines or operations present potential eye or face injury."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "E",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 1,
    },
    {
        "standard_id": "1926.102(a)(2)",
        "title": "Eye Protection - Prescription Lenses",
        "description": (
            "Eye protection equipment that provides side protection shall be used when "
            "there is a hazard from flying objects."
        ),
        "severity": SeverityLevel.OTHER_THAN_SERIOUS,
        "subpart": "E",
        "penalty_min": 0,
        "penalty_max": 15625,
        "abatement_days": 7,
    },
    # Subpart F - Fire Protection and Prevention
    {
        "standard_id": "1926.150(a)",
        "title": "Fire Protection - General Requirements",
        "description": (
            "The employer shall be responsible for the development of a fire protection "
            "program throughout all phases of construction and demolition work."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "F",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 15,
    },
    {
        "standard_id": "1926.152(a)(1)",
        "title": "Flammable Liquids - Storage",
        "description": (
            "Only approved containers and portable tanks shall be used for storage "
            "and handling of flammable liquids."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "F",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 7,
    },
    # Subpart G - Signs, Signals, and Barricades
    {
        "standard_id": "1926.200(a)",
        "title": "Accident Prevention Signs and Tags",
        "description": "Signs and symbols shall be visible at all times when work is being performed.",
        "severity": SeverityLevel.OTHER_THAN_SERIOUS,
        "subpart": "G",
        "penalty_min": 0,
        "penalty_max": 15625,
        "abatement_days": 7,
    },
    {
        "standard_id": "1926.201(a)",
        "title": "Signaling - Flaggers",
        "description": (
            "When operations are such that signs, signals, and barricades do not provide "
            "the necessary protection on or adjacent to a highway, flaggers or other "
            "appropriate traffic controls shall be provided."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "G",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 1,
    },
    # Subpart K - Electrical
    {
        "standard_id": "1926.404(b)(1)(i)",
        "title": "GFCI Protection",
        "description": (
            "All 120-volt, single-phase, 15- and 20-ampere receptacle outlets on "
            "construction sites which are not a part of the permanent wiring of the "
            "building shall have approved ground-fault circuit interrupters."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "K",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 7,
    },
    {
        "standard_id": "1926.405(a)(2)(ii)(I)",
        "title": "Electrical - Flexible Cords and Cables",
        "description": (
            "Flexible cords and cables shall be protected from accidental damage. "
            "Sharp corners and projections shall be avoided."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "K",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 7,
    },
    {
        "standard_id": "1926.416(a)(1)",
        "title": "Electrical - Safety-Related Work Practices",
        "description": (
            "No employer shall permit an employee to work in such proximity to any part "
            "of an electric power circuit that the employee could contact the circuit."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "K",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 1,
    },
    # Subpart L - Scaffolds
    {
        "standard_id": "1926.451(a)(1)",
        "title": "Scaffolds - Capacity",
        "description": (
            "Each scaffold and scaffold component shall be capable of supporting, "
            "without failure, its own weight and at least 4 times the maximum intended load."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "L",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 1,
    },
    {
        "standard_id": "1926.451(b)(1)",
        "title": "Scaffolds - Platform Construction",
        "description": (
            "Each scaffold platform and walkway shall be at least 18 inches wide. "
            "Each scaffold plank shall extend over its end supports not less than "
            "6 inches nor more than 12 inches."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "L",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 1,
    },
    {
        "standard_id": "1926.451(g)(1)",
        "title": "Scaffolds - Fall Protection",
        "description": (
            "Each employee on a scaffold more than 10 feet above a lower level shall be "
            "protected from falling by guardrails or a personal fall arrest system."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "L",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 1,
    },
    {
        "standard_id": "1926.454(a)",
        "title": "Scaffold Training",
        "description": (
            "The employer shall have each employee who performs work on a scaffold trained "
            "by a qualified person to recognize the hazards associated with the type of "
            "scaffold being used."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "L",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 15,
    },
    # Subpart M - Fall Protection
    {
        "standard_id": "1926.501(b)(1)",
        "title": "Fall Protection - Unprotected Sides and Edges",
        "description": (
            "Each employee on a walking/working surface with an unprotected side or edge "
            "which is 6 feet or more above a lower level shall be protected from falling "
            "by guardrail, safety net, or personal fall arrest system."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "M",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 1,
    },
    {
        "standard_id": "1926.501(b)(10)",
        "title": "Fall Protection - Roofing Work on Low-Slope Roofs",
        "description": (
            "Each employee engaged in roofing activities on low-slope roofs with "
            "unprotected sides and edges 6 feet or more above lower levels shall be "
            "protected by guardrail, safety net, or personal fall arrest systems."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "M",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 1,
    },
    {
        "standard_id": "1926.501(b)(13)",
        "title": "Fall Protection - Residential Construction",
        "description": (
            "Each employee engaged in residential construction 6 feet or more above "
            "lower levels shall be protected by conventional fall protection or by "
            "alternative measures."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "M",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 1,
    },
    {
        "standard_id": "1926.502(b)(1)",
        "title": "Guardrail Systems - Top Rail Height",
        "description": (
            "Top edge height of top rails shall be 42 inches plus or minus 3 inches "
            "above the walking/working level."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "M",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 1,
    },
    {
        "standard_id": "1926.502(b)(3)",
        "title": "Guardrail Systems - Mid Rails",
        "description": (
            "When mid-rails are used they shall be installed at a height midway between "
            "the top edge of the guardrail system and the walking/working surface."
        ),
        "severity": SeverityLevel.OTHER_THAN_SERIOUS,
        "subpart": "M",
        "penalty_min": 0,
        "penalty_max": 15625,
        "abatement_days": 7,
    },
    {
        "standard_id": "1926.502(b)(4)",
        "title": "Guardrail Systems - Strength",
        "description": (
            "Guardrail systems shall be capable of withstanding, without failure, "
            "a force of at least 200 pounds applied within 2 inches of the top edge "
            "in any outward or downward direction."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "M",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 1,
    },
    {
        "standard_id": "1926.502(d)",
        "title": "Personal Fall Arrest Systems",
        "description": (
            "Personal fall arrest systems shall limit maximum arresting force on an "
            "employee to 1,800 pounds when used with a body harness."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "M",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 1,
    },
    {
        "standard_id": "1926.503(a)(1)",
        "title": "Fall Protection Training",
        "description": (
            "The employer shall provide a training program for each employee who might "
            "be exposed to fall hazards, enabling the employee to recognize the hazards "
            "and the procedures to minimize them."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "M",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 15,
    },
    # Subpart P - Excavations
    {
        "standard_id": "1926.651(a)",
        "title": "Excavations - Underground Installations",
        "description": (
            "The estimated location of utility installations that reasonably may be "
            "expected to be encountered shall be determined prior to opening an excavation."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "P",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 1,
    },
    {
        "standard_id": "1926.652(a)(1)",
        "title": "Excavations - Protection of Employees",
        "description": (
            "Each employee in an excavation shall be protected from cave-ins by an "
            "adequate protective system when the excavation is 5 feet or more in depth."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "P",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 1,
    },
    # Subpart R - Steel Erection
    {
        "standard_id": "1926.760(a)",
        "title": "Steel Erection - Fall Protection",
        "description": (
            "Each employee engaged in a steel erection activity on a walking/working "
            "surface with an unprotected side or edge more than 15 feet above a lower "
            "level shall be protected by guardrail, safety net, personal fall arrest, "
            "positioning device, or fall restraint systems."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "R",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 1,
    },
    # Subpart X - Stairways and Ladders
    {
        "standard_id": "1926.1050(a)",
        "title": "Stairways and Ladders - Scope",
        "description": (
            "A stairway or ladder shall be provided at all personnel points of access "
            "where there is a break in elevation of 19 inches or more."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "X",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 7,
    },
    {
        "standard_id": "1926.1053(a)(4)",
        "title": "Ladders - Non-Self-Supporting",
        "description": (
            "Non-self-supporting ladders shall be used at an angle such that the "
            "horizontal distance from the top support to the foot is approximately "
            "one-quarter of the working length."
        ),
        "severity": SeverityLevel.OTHER_THAN_SERIOUS,
        "subpart": "X",
        "penalty_min": 0,
        "penalty_max": 15625,
        "abatement_days": 7,
    },
    {
        "standard_id": "1926.1053(b)(1)",
        "title": "Ladders - Use",
        "description": (
            "When portable ladders are used for access to an upper landing surface, "
            "the side rails shall extend at least 3 feet above the upper landing surface."
        ),
        "severity": SeverityLevel.SERIOUS,
        "subpart": "X",
        "penalty_min": 1036,
        "penalty_max": 15625,
        "abatement_days": 7,
    },
]


class OSHAStandards:
    """Database of real OSHA construction safety standards (29 CFR 1926).

    Contains 30+ frequently cited standards covering head protection, fall
    protection, scaffolding, electrical safety, excavations, and more.
    """

    def __init__(self) -> None:
        self._standards: dict[str, OSHAViolation] = {}
        for entry in _STANDARDS:
            violation = OSHAViolation(**entry)
            self._standards[entry["standard_id"]] = violation

    def get_standard(self, standard_id: str) -> Optional[OSHAViolation]:
        """Look up a standard by its ID (e.g. '1926.100(a)')."""
        return self._standards.get(standard_id)

    def list_all(self) -> list[OSHAViolation]:
        """Return all standards in the database."""
        return list(self._standards.values())

    def list_by_subpart(self, subpart: str) -> list[OSHAViolation]:
        """Return standards filtered by subpart letter."""
        return [v for v in self._standards.values() if v.subpart == subpart.upper()]

    def list_by_severity(self, severity: SeverityLevel) -> list[OSHAViolation]:
        """Return standards filtered by severity level."""
        return [v for v in self._standards.values() if v.severity == severity]

    def search(self, keyword: str) -> list[OSHAViolation]:
        """Search standards by keyword in title or description."""
        keyword_lower = keyword.lower()
        return [
            v
            for v in self._standards.values()
            if keyword_lower in v.title.lower() or keyword_lower in v.description.lower()
        ]

    @property
    def count(self) -> int:
        """Total number of standards in the database."""
        return len(self._standards)
