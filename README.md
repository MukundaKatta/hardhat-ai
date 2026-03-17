# Hardhat-AI

Construction Safety Compliance Checker powered by AI.

Hardhat-AI uses computer vision and rule-based engines to detect PPE compliance,
identify construction site hazards, and map findings to real OSHA standards with
penalty calculations.

## Features

- **PPE Detection**: CNN-based detection of hard hats, vests, goggles, gloves, boots, and harnesses
- **Hazard Identification**: Detects unguarded edges, missing guardrails, improper scaffolding, and electrical hazards
- **OSHA Compliance Mapping**: Maps detections to 30+ real OSHA construction standards (29 CFR 1926)
- **Penalty Calculation**: Computes fines using official OSHA penalty schedules
- **Inspection Protocols**: Daily, weekly, and monthly safety check workflows
- **Rich Reports**: Generate detailed inspection reports with violation summaries

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Run a simulated inspection
hardhat inspect --site "Building A" --type daily

# Check an image for PPE compliance
hardhat check-ppe --image site_photo.jpg

# Scan for hazards
hardhat scan-hazards --image site_photo.jpg

# Generate a compliance report
hardhat report --site "Building A" --output report.html
```

## OSHA Standards Coverage

Covers standards from 29 CFR 1926 including:
- Subpart C: General Safety and Health Provisions
- Subpart D: Occupational Health and Environmental Controls
- Subpart E: Personal Protective and Life Saving Equipment
- Subpart K: Electrical
- Subpart L: Scaffolds
- Subpart M: Fall Protection
- Subpart P: Excavations
- Subpart R: Steel Erection
- Subpart X: Stairways and Ladders

## Author

Mukunda Katta
