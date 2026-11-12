"""Parameter presets for the sample photos and generic images."""

from dataclasses import dataclass
from pathlib import Path

from .detector import HoughParams


@dataclass(frozen=True)
class Preset:
    key: str
    label: str
    params: HoughParams


COINS = Preset(
    key="coins",
    label="硬币",
    params=HoughParams(
        dp=1.2, min_dist=250, param1=100, param2=30, min_radius=120, max_radius=200
    ),
)

COOKIE_PLATE = Preset(
    key="cookie_plate",
    label="饼干盘",
    params=HoughParams(
        dp=1.2, min_dist=250, param1=100, param2=30, min_radius=200, max_radius=270
    ),
)

PRESETS = (COINS, COOKIE_PLATE)


def preset_for_path(path: str | Path) -> Preset | None:
    """Match a preset by filename; return None for unknown images."""
    name = Path(path).name.lower()
    if "coin" in name:
        return COINS
    if "cookie" in name or "plate" in name:
        return COOKIE_PLATE
    return None


def generic_params(width: int, height: int) -> HoughParams:
    """Reasonable radius and spacing defaults for an arbitrary image size."""
    if width <= 0 or height <= 0:
        raise ValueError("image dimensions must be positive")

    short_side = min(width, height)
    return HoughParams(
        dp=1.2,
        min_dist=max(20, short_side // 3),
        param1=100,
        param2=30,
        min_radius=max(1, short_side // 10),
        max_radius=max(2, short_side // 2),
    )
