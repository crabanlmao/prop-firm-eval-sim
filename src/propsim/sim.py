import numpy as np


def eval_path(net, low, rules, per_point, horizon=None):
    bal = peak = rules.start_balance
    floor = rules.start_balance - rules.trailing_dd
    best_day = 0.0
    n = len(net) if horizon is None else min(horizon, len(net))
    for i in range(n):
        day = net[i] * per_point
        intraday_low = bal + low[i] * per_point
        if rules.daily_loss > 0 and bal - intraday_low >= rules.daily_loss:
            return "bust", i + 1
        if intraday_low <= floor:
            return "bust", i + 1
        bal += day
        best_day = max(best_day, day)
        if bal > peak:
            peak = bal
            floor = min(rules.start_balance, peak - rules.trailing_dd)
        profit = bal - rules.start_balance
        if profit >= rules.profit_target and i + 1 >= rules.min_days:
            if rules.consistency <= 0 or best_day <= rules.consistency * profit:
                return "pass", i + 1
    return "timeout", n


def walk_forward(net, low, rules, per_point, horizon):
    return [eval_path(net[s:], low[s:], rules, per_point, horizon) for s in range(len(net))]


def block_bootstrap(net, low, rules, per_point, horizon, n_paths=5000, block=5, seed=0):
    rng = np.random.default_rng(seed)
    n = len(net)
    out = []
    for _ in range(n_paths):
        starts = rng.integers(0, n, size=-(-horizon // block))
        idx = np.concatenate([(np.arange(s, s + block) % n) for s in starts])[:horizon]
        out.append(eval_path(net[idx], low[idx], rules, per_point, horizon))
    return out


def summarize(results):
    outcome = np.array([o for o, _ in results])
    days = np.array([d for _, d in results])
    passed = outcome == "pass"
    return {"p_pass": float(passed.mean()), "p_bust": float((outcome == "bust").mean()),
            "p_timeout": float((outcome == "timeout").mean()),
            "days_to_pass": float(days[passed].mean()) if passed.any() else float("nan"),
            "n": len(results)}


def size_sweep(net, low, rules, per_point=2.0, sizes=range(1, 21), horizon=120, method="walk_forward", **kw):
    rows = []
    for c in sizes:
        res = (walk_forward(net, low, rules, per_point * c, horizon) if method == "walk_forward"
               else block_bootstrap(net, low, rules, per_point * c, horizon, **kw))
        rows.append({"contracts": c, **summarize(res)})
    return rows
