"""Construction site hazard detection."""

from __future__ import annotations

from typing import Optional

import torch
import torch.nn as nn

from hardhat.models import HazardDetection, HazardType


class HazardDetectorCNN(nn.Module):
    """CNN for detecting construction site hazards.

    Identifies: unguarded edges, missing guardrails, improper scaffolding,
    and electrical hazards.
    """

    HAZARD_CLASSES = [
        HazardType.UNGUARDED_EDGES,
        HazardType.MISSING_GUARDRAILS,
        HazardType.IMPROPER_SCAFFOLDING,
        HazardType.ELECTRICAL_HAZARDS,
    ]

    def __init__(self) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((1, 1)),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.4),
            nn.Linear(256, len(self.HAZARD_CLASSES)),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.classifier(x)
        return torch.sigmoid(x)


# Descriptions for detected hazards
HAZARD_DESCRIPTIONS: dict[HazardType, str] = {
    HazardType.UNGUARDED_EDGES: (
        "Unprotected sides or edges detected where workers could fall 6 feet or more. "
        "Per OSHA 1926.501(b)(1), each employee on a walking/working surface with an "
        "unprotected side or edge 6 feet or more above a lower level shall be protected "
        "by guardrail systems, safety net systems, or personal fall arrest systems."
    ),
    HazardType.MISSING_GUARDRAILS: (
        "Guardrail system absent or non-compliant. Per OSHA 1926.502(b), guardrails must "
        "have a top rail at 42 inches (+/- 3 inches), a mid rail, and withstand 200 lbs "
        "of force applied in any outward or downward direction."
    ),
    HazardType.IMPROPER_SCAFFOLDING: (
        "Scaffold does not meet OSHA requirements. Per OSHA 1926.451, scaffolds must be "
        "erected on sound footing, fully planked, and equipped with guardrails when the "
        "platform is more than 10 feet above the ground."
    ),
    HazardType.ELECTRICAL_HAZARDS: (
        "Electrical hazard identified. Per OSHA 1926.405, all electrical equipment and "
        "installations must comply with applicable requirements. Exposed wiring, damaged "
        "cords, and missing GFCIs are common violations."
    ),
}


class HazardDetector:
    """High-level hazard detection interface."""

    DETECTION_THRESHOLD = 0.5

    def __init__(self, model_path: Optional[str] = None) -> None:
        self.model = HazardDetectorCNN()
        self.model.eval()
        if model_path is not None:
            state_dict = torch.load(model_path, map_location="cpu", weights_only=True)
            self.model.load_state_dict(state_dict)
        self.classes = HazardDetectorCNN.HAZARD_CLASSES

    def detect(self, image_tensor: torch.Tensor) -> list[HazardDetection]:
        """Run hazard detection on an image tensor.

        Args:
            image_tensor: Tensor of shape (1, 3, 224, 224) or (3, 224, 224).

        Returns:
            List of HazardDetection results.
        """
        if image_tensor.dim() == 3:
            image_tensor = image_tensor.unsqueeze(0)

        with torch.no_grad():
            predictions = self.model(image_tensor)

        detections: list[HazardDetection] = []
        for i, hazard_type in enumerate(self.classes):
            confidence = float(predictions[0, i])
            detections.append(
                HazardDetection(
                    hazard_type=hazard_type,
                    detected=confidence >= self.DETECTION_THRESHOLD,
                    confidence=round(confidence, 4),
                    location_description=HAZARD_DESCRIPTIONS.get(hazard_type, ""),
                )
            )
        return detections

    def get_detected_hazards(self, image_tensor: torch.Tensor) -> list[HazardDetection]:
        """Return only hazards that were positively detected."""
        return [d for d in self.detect(image_tensor) if d.detected]

    def assess_risk_level(self, detections: list[HazardDetection]) -> str:
        """Assess overall site risk based on detected hazards.

        Returns:
            Risk level string: 'low', 'medium', 'high', or 'critical'.
        """
        detected = [d for d in detections if d.detected]
        if not detected:
            return "low"

        high_risk = {HazardType.UNGUARDED_EDGES, HazardType.ELECTRICAL_HAZARDS}
        has_high_risk = any(d.hazard_type in high_risk for d in detected)

        if len(detected) >= 3 or has_high_risk:
            return "critical" if len(detected) >= 3 and has_high_risk else "high"
        if len(detected) >= 2:
            return "medium"
        return "medium" if detected[0].confidence > 0.8 else "low"
