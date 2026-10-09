import numpy as np

from propsim import PRESETS, Rules, eval_path, walk_forward, block_bootstrap, summarize, size_sweep, synthetic_days

R = PRESETS["50K"]


def test_steady_winner_passes():
    net = np.full(30, 20.0)
    low = np.zeros(30)
    assert eval_path(net, low, R, per_point=10)[0] == "pass"


def test_drawdown_breach_intraday_busts():
    net = np.array([5.0, 5.0, 5.0])
    low = np.array([-1.0, -1.0, -250.0])
    assert eval_path(net, low, R, per_point=10)[0] == "bust"


def test_floor_ratchets_up_with_the_peak():
    rules = Rules(50_000, 2_000, 99_999)
    net = np.array([20.0, 20.0, 0.0])
    assert eval_path(net, np.array([0.0, 0.0, -190.0]), rules, per_point=10)[0] == "timeout"
    assert eval_path(net, np.array([0.0, 0.0, -210.0]), rules, per_point=10)[0] == "bust"


def test_floor_locks_at_start_balance():
    rules = Rules(50_000, 2_000, 99_999)
    net = np.array([300.0, 300.0, -1.0])
    assert eval_path(net, np.array([0.0, 0.0, -250.0]), rules, per_point=10)[0] == "timeout"
    assert eval_path(net, np.array([0.0, 0.0, -700.0]), rules, per_point=10)[0] == "bust"


def test_consistency_rule_blocks_a_one_big_day_pass():
    net = np.array([1.0, 1.0, 1.0, 400.0])
    low = np.zeros(4)
    assert eval_path(net, low, R, per_point=10)[0] == "timeout"
    assert eval_path(net, low, Rules(50_000, 2_000, 3_000, consistency=0), per_point=10)[0] == "pass"


def test_daily_loss_limit():
    rules = Rules(50_000, 2_000, 3_000, daily_loss=500)
    assert eval_path(np.array([-10.0]), np.array([-60.0]), rules, per_point=10)[0] == "bust"


def test_walk_forward_covers_every_start():
    net, low = synthetic_days(seed=1)
    assert len(walk_forward(net, low, R, 20.0, 120)) == len(net)


def test_walk_forward_is_harsher_than_bootstrap_when_the_edge_arrives_late():
    net, low = synthetic_days(seed=2)
    wf = summarize(walk_forward(net[:120], low[:120], R, 20.0, 120))
    bs = summarize(block_bootstrap(net, low, R, 20.0, 120, n_paths=800, seed=3))
    assert bs["p_pass"] > wf["p_pass"]


def test_bigger_size_busts_more():
    net, low = synthetic_days(seed=4)
    rows = size_sweep(net, low, R, sizes=[2, 30], method="bootstrap", n_paths=400, seed=5)
    assert rows[1]["p_bust"] > rows[0]["p_bust"]
