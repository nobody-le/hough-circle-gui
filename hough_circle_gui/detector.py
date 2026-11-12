"""OpenCV Hough circle detection, independent of the GUI."""

from dataclasses import dataclass

import cv2
import numpy as np

Circle = tuple[int, int, int]


@dataclass(frozen=True)
class HoughParams:
    """Parameters passed to cv2.HoughCircles."""

    dp: float = 1.2
    min_dist: int = 250
    param1: int = 100
    param2: int = 30
    min_radius: int = 120
    max_radius: int = 200

    def __post_init__(self) -> None:
        if self.dp <= 0:
            raise ValueError("dp must be positive")
        if self.min_dist <= 0:
            raise ValueError("min_dist must be positive")
        if self.param1 <= 0 or self.param2 <= 0:
            raise ValueError("param1 and param2 must be positive")
        if self.min_radius < 0 or self.max_radius <= self.min_radius:
            raise ValueError("radius range must satisfy 0 <= min < max")


def detect_circles(image: np.ndarray, params: HoughParams) -> list[Circle]:
    """Return detected circles as (x, y, radius), largest first not guaranteed."""
    if image is None or image.size == 0:
        raise ValueError("image is empty")

    if image.ndim == 2:
        gray = image
    elif image.ndim == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        raise ValueError("image must be grayscale or BGR")

    blurred = cv2.medianBlur(gray, 5)
    found = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=params.dp,
        minDist=params.min_dist,
        param1=params.param1,
        param2=params.param2,
        minRadius=params.min_radius,
        maxRadius=params.max_radius,
    )
    if found is None:
        return []

    return [
        (int(round(float(x))), int(round(float(y))), int(round(float(radius))))
        for x, y, radius in found[0]
    ]


def annotate_image(image: np.ndarray, circles: list[Circle]) -> np.ndarray:
    """Draw circles, centers and indices on a copy of the image."""
    if image is None or image.size == 0:
        raise ValueError("image is empty")

    annotated = image.copy()
    for index, (x, y, radius) in enumerate(circles, start=1):
        cv2.circle(annotated, (x, y), radius, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.circle(annotated, (x, y), 4, (0, 0, 255), -1, cv2.LINE_AA)

        label = str(index)
        (text_width, text_height), _ = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2
        )
        text_x = max(0, min(annotated.shape[1] - text_width - 2, x - text_width // 2))
        text_y = max(text_height + 2, y - radius - 8)
        cv2.putText(
            annotated,
            label,
            (text_x, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )

    return annotated
