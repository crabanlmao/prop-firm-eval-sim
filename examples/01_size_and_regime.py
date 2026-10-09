from propsim import PRESETS, size_sweep, synthetic_days, walk_forward, block_bootstrap, summarize

net, low = synthetic_days(seed=2)
rules = PRESETS["50K"]

print("contracts  pass   bust   days")
for r in size_sweep(net, low, rules, sizes=[2, 4, 6, 8, 10, 14, 20], method="bootstrap", n_paths=2000):
    print(f"{r['contracts']:9d}  {r['p_pass']:.0%}  {r['p_bust']:5.0%}  {r['days_to_pass']:5.1f}")

print()
for name, a, b in (("first regime (no edge)", 0, 120), ("second regime (edge)", 120, 240)):
    s = summarize(walk_forward(net[a:b], low[a:b], rules, 2.0 * 6, 120))
    print(f"{name:24s} 6 contracts: pass {s['p_pass']:.0%}, bust {s['p_bust']:.0%}")
s = summarize(block_bootstrap(net, low, rules, 2.0 * 6, 120, n_paths=2000))
print(f"{'bootstrap, regimes mixed':24s} 6 contracts: pass {s['p_pass']:.0%}, bust {s['p_bust']:.0%}")
