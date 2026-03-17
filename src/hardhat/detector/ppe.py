"""PPE (Personal Protective Equipment) detection using CNN."""

from __future__ import annotations

from typing import Optional

import torch
import torch.nn as nn

from hardhat.models import PPEDetection, PPEType


class PPEDetectorCNN(nn.Module):
    """Convolutional Neural Network for PPE detection.

    Detects six types of PPE: hard hat, vest, goggles, gloves, boots, harness.
    Input: 224x224 RGB image tensors.
    Output: 6-class multi-label predictions.
    """

    PPE_CLASSES = [
        PPEType.HARD_HAT,
        PPEType.VEST,
        PPEType.GOGGLES,
        PPEType.GLOVES,
        PPEType.BOOTS,
        PPEType.HARNESS,
    ]

    def __init__(self) -> None:
        super().__init__()
        self.features = nn.Sequential(
            # Block 1: 224x224 -> 112x112
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            # Block 2: 112x112 -> 56x56
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            # Block 3: 56x56 -> 28x28
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            # Block 4: 28x28 -> 14x14
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            # Block 5: 14x14 -> 7x7
            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
        )
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(512, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(256, len(self.PPE_CLASSES)),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.classifier(x)
        return torch.sigmoid(x)


class PPEDetector:
    """High-level PPE detection interface wrapping the CNN model."""

    DETECTION_THRESHOLD = 0.5

    def __init__(self, model_path: Optional[str] = None) -> None:
        self.model = PPEDetectorCNN()
        self.model.eval()
        if model_path is not None:
            state_dict = torch.load(model_path, map_location="cpu", weights_only=True)
            self.model.load_state_dict(state_dict)
        self.classes = PPEDetectorCNN.PPE_CLASSES

    def detect(self, image_tensor: torch.Tensor) -> list[PPEDetection]:
        """Run PPE detection on an image tensor.

        Args:
            image_tensor: A tensor of shape (1, 3, 224, 224) or (3, 224, 224).

        Returns:
            List of PPEDetection results for each PPE class.
        """
        if image_tensor.dim() == 3:
            image_tensor = image_tensor.unsqueeze(0)

        with torch.no_grad():
            predictions = self.model(image_tensor)

        detections: list[PPEDetection] = []
        for i, ppe_type in enumerate(self.classes):
            confidence = float(predictions[0, i])
            detections.append(
                PPEDetection(
                    ppe_type=ppe_type,
                    detected=confidence >= self.DETECTION_THRESHOLD,
                    confidence=round(confidence, 4),
                )
            )
        return detections

    def detect_missing_ppe(
        self, image_tensor: torch.Tensor, required: Optional[list[PPEType]] = None
    ) -> list[PPEDetection]:
        """Detect which required PPE items are missing.

        Args:
            image_tensor: Image tensor to analyze.
            required: List of required PPE types. Defaults to all types.

        Returns:
            List of PPEDetection results for missing items only.
        """
        if required is None:
            required = list(PPEType)

        all_detections = self.detect(image_tensor)
        return [d for d in all_detections if d.ppe_type in required and not d.detected]

    def get_compliance_summary(self, detections: list[PPEDetection]) -> dict[str, bool]:
        """Get a summary of PPE compliance."""
        return {d.ppe_type.value: d.detected for d in detections}
