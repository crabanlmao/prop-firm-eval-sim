# prop-firm-eval-sim

Pass and bust probability for a prop firm evaluation, from a daily P&L sequence. The question is whether the account hits the profit target before the trailing drawdown, not what the equity curve looks like.

Handles an end-of-day trailing floor that locks at the starting balance, intraday breach checks, a best-day consistency rule, a daily loss limit and a minimum number of days. Path generators are walk-forward (every real start date) and block bootstrap.

```bash
pip install -e ".[dev]"
python -m pytest
python examples/01_size_and_regime.py
```

Synthetic example, 50K account, MNQ at $2/point, 120 no-edge days followed by 120 days with edge:

| contracts | pass | bust |
|---|---|---|
| 4 | 4% | 0% |
| 8 | 56% | 4% |
| 10 | 69% | 11% |
| 14 | 72% | 25% |
| 20 | 60% | 40% |

Size scales profit and drawdown together, so past a point more contracts only busts faster. At 6 contracts, starting in the no-edge period passes 0%, starting in the edge period 45%, and the mixed bootstrap 28%. The bootstrap can't know the edge arrives late, so it flatters a regime-dependent strategy. Walk-forward is the honest view.

I ran the same logic on my own NinjaTrader MNQ scalper (data not included): 162 trades, +272.7 net points after commission, but +31.4 in 2025 and +241.2 in 2026. Walk-forward passed 87% at 8 contracts with 0% bust, while a 2025-only bootstrap passed 35% and busted 55%. It is a regime bet and I treat it as one.

Preset rules are the 2026 values I pulled for Topstep and Lucid evaluations. Check the current rules before relying on them.
