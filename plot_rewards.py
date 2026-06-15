import pandas as pd
import matplotlib.pyplot as plt

files = {
    "mean_reward":      ("data/g1_2026-06-14_mean_reward.csv",      "Mean Reward",                "#2563eb"),
    "error_vel_xy":     ("data/g1_2026-06-14_error_vel_xy.csv",     "Velocity Error (xy)",        "#dc2626"),
    "flat_orientation": ("data/g1_2026-06-14_flat_orientation_l2.csv", "Flat Orientation (penalty)", "#16a34a"),
    "feet_air_time":    ("data/g1_2026-06-14_feet_air_time.csv",    "Feet Air Time",              "#9333ea"),
    "feet_slide":       ("data/g1_2026-06-14_feet_slide.csv",       "Feet Slide (penalty)",       "#ea580c"),
    "action_rate":      ("data/g1_2026-06-14_action_rate_l2.csv",   "Action Rate (penalty)",      "#0891b2"),
}

def load(path):
    df = pd.read_csv(path)
    df["smooth"] = df["Value"].rolling(10, min_periods=1).mean()
    return df

# 포폴용 3개: 각각 단독 PNG
portfolio = ["mean_reward", "error_vel_xy", "flat_orientation"]
for key in portfolio:
    path, label, color = files[key]
    df = load(path)
    plt.figure(figsize=(7, 4.5))
    plt.plot(df["Step"], df["Value"], color=color, alpha=0.25, linewidth=1)
    plt.plot(df["Step"], df["smooth"], color=color, linewidth=2.2, label=label)
    plt.title(f"G1 Locomotion Training — {label}", fontsize=13, fontweight="bold")
    plt.xlabel("Training Iteration")
    plt.ylabel(label)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"portfolio_{key}.png", dpi=200)
    plt.close()
    print(f"saved: portfolio_{key}.png")

# 나머지 3개: 참고용 한 장
others = ["feet_air_time", "feet_slide", "action_rate"]
fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, key in zip(axes, others):
    path, label, color = files[key]
    df = load(path)
    ax.plot(df["Step"], df["smooth"], color=color, linewidth=2)
    ax.set_title(label, fontsize=11)
    ax.set_xlabel("Iteration")
    ax.grid(alpha=0.3)
fig.suptitle("Auxiliary Reward Terms (reference)", fontsize=13, fontweight="bold")
fig.tight_layout()
fig.savefig("aux_terms.png", dpi=200)
print("saved: aux_terms.png")
