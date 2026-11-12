import unittest
from pathlib import Path

import cv2
import numpy as np

from hough_circle_gui.detector import HoughParams, annotate_image, detect_circles
from hough_circle_gui.presets import (
    COINS,
    COOKIE_PLATE,
    generic_params,
    preset_for_path,
)

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "examples"


class DetectorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.coins = cv2.imread(str(EXAMPLES / "coins.jpg"))
        cls.plate = cv2.imread(str(EXAMPLES / "cookie-plate.jpg"))
        if cls.coins is None or cls.plate is None:
            raise RuntimeError("sample images are missing")

    def test_coins_preset_finds_two_outer_edges(self) -> None:
        circles = detect_circles(self.coins, COINS.params)

        self.assertEqual(len(circles), 2)
        centers_x = sorted(x for x, _, _ in circles)
        self.assertLess(centers_x[0], 300)
        self.assertGreater(centers_x[1], 400)
        self.assertTrue(all(150 <= radius <= 210 for _, _, radius in circles))

    def test_cookie_plate_preset_finds_one_rim(self) -> None:
        circles = detect_circles(self.plate, COOKIE_PLATE.params)

        self.assertEqual(len(circles), 1)
        x, y, radius = circles[0]
        self.assertAlmostEqual(x, 263, delta=12)
        self.assertAlmostEqual(y, 259, delta=12)
        self.assertTrue(220 <= radius <= 260)

    def test_annotation_keeps_shape_and_draws(self) -> None:
        circles = detect_circles(self.coins, COINS.params)
        annotated = annotate_image(self.coins, circles)

        self.assertEqual(annotated.shape, self.coins.shape)
        self.assertFalse(np.array_equal(annotated, self.coins))

    def test_empty_image_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            detect_circles(np.zeros((0, 0, 3), dtype=np.uint8), COINS.params)

    def test_invalid_radius_range_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            HoughParams(min_radius=100, max_radius=50)

    def test_filename_presets(self) -> None:
        self.assertIs(preset_for_path("coins.jpg"), COINS)
        self.assertIs(preset_for_path("cookie-plate.jpg"), COOKIE_PLATE)
        self.assertIsNone(preset_for_path("street.jpg"))

    def test_generic_params_are_valid(self) -> None:
        params = generic_params(760, 385)

        self.assertLess(params.min_radius, params.max_radius)
        self.assertGreater(params.min_dist, 0)


if __name__ == "__main__":
    unittest.main()
