from dataclasses import dataclass


@dataclass(frozen=True)
class Rules:
    start_balance: float
    trailing_dd: float
    profit_target: float
    consistency: float = 0.5
    daily_loss: float = 0.0
    min_days: int = 2


PRESETS = {
    "50K": Rules(50_000, 2_000, 3_000),
    "100K": Rules(100_000, 3_000, 6_000),
    "150K": Rules(150_000, 4_500, 9_000),
}
