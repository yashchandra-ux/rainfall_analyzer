"""Rainfall Data Analyzer - NumPy, Pandas, Matplotlib."""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

HEAVY_MM = 200


def load_data(path):
    """Load CSV (Month, Rainfall_mm); skip invalid rows with messages."""
    try:
        raw = pd.read_csv(path, header=None, names=["Month", "Rainfall_mm"],
                          dtype=str, skipinitialspace=True)
    except FileNotFoundError:
        print(f"File '{path}' not found.")
        return None
    except pd.errors.EmptyDataError:
        print("File is empty.")
        return None

    # Drop header row if present
    if len(raw) and str(raw.iloc[0, 0]).strip().lower() == "month":
        raw = raw.iloc[1:]
    raw = raw.reset_index(drop=True)

    months, values = [], []
    for i, row in raw.iterrows():
        n = i + 1
        month = row["Month"]
        val = row["Rainfall_mm"]
        if pd.isna(month) or pd.isna(val) or str(val).strip() == "":
            print(f"Row {n} skipped: missing value.")
            continue
        try:
            x = float(str(val).strip())
        except ValueError:
            print(f"Row {n} skipped: invalid Rainfall '{str(val).strip()}'.")
            continue
        if x < 0:
            print(f"Row {n} skipped: Rainfall cannot be negative.")
            continue
        months.append(str(month).strip())
        values.append(x)

    df = pd.DataFrame({"Month": months, "Rainfall_mm": values})
    print(f"Valid rows: {len(df)} | Total: {df['Rainfall_mm'].sum():g} mm")
    return df


def statistics(df):
    r = df["Rainfall_mm"].to_numpy()
    total, mean = np.sum(r), np.mean(r)
    std = np.std(r)  # population std (default)
    imax, imin = np.argmax(r), np.argmin(r)
    print(f"Total: {total:g} mm | Mean: {mean:.2f}")
    print(f"Max: {df['Month'][imax]} ({r[imax]:g}) | "
          f"Min: {df['Month'][imin]} ({r[imin]:g})")
    print(f"Std Dev: {std:.2f}")
    heavy = df[df["Rainfall_mm"] > HEAVY_MM]["Month"].tolist()
    if heavy:
        print("Heavy rainfall months: " + ", ".join(heavy))
    else:
        print(f"No month above {HEAVY_MM} mm")


def compare_and_plot(df):
    mean = df["Rainfall_mm"].mean()
    above = df[df["Rainfall_mm"] > mean]
    below = df[df["Rainfall_mm"] <= mean]
    fmt = lambda d: " | ".join(f"{m} ({v:g})" for m, v in
                               zip(d["Month"], d["Rainfall_mm"])) or "None"
    print(f"Above average ({mean:.2f}): {fmt(above)}")
    print(f"Below average: {fmt(below)}")

    plt.figure(figsize=(7, 4))
    colors = ["tab:blue" if v > mean else "tab:orange" for v in df["Rainfall_mm"]]
    plt.bar(df["Month"], df["Rainfall_mm"], color=colors)
    plt.axhline(mean, color="red", linestyle="--", label=f"Average ({mean:.2f})")
    plt.title("Monthly Rainfall")
    plt.xlabel("Month")
    plt.ylabel("Rainfall (mm)")
    plt.legend()
    plt.tight_layout()
    print("Bar chart 'Monthly Rainfall' displayed")
    plt.show()


def trend_plot(df):
    plt.figure(figsize=(7, 4))
    plt.plot(df["Month"], df["Rainfall_mm"], marker="o")
    plt.title("Rainfall Trend")
    plt.xlabel("Month")
    plt.ylabel("Rainfall (mm)")
    plt.grid(True)
    plt.tight_layout()
    print("Line chart 'Rainfall Trend' displayed")
    plt.show()


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "rain.csv"
    df = load_data(path)
    if df is None or df.empty:
        print("No valid data to analyse.")
        return
    while True:
        print("\n1. Statistics\n2. Heavy rainfall months\n"
              "3. Compare with average and plot\n4. Trend line chart\n5. Exit")
        choice = input("Choose option: ").strip()
        if choice == "1":
            statistics(df)
        elif choice == "2":
            heavy = df[df["Rainfall_mm"] > HEAVY_MM]
            print("Heavy rainfall months: " + ", ".join(heavy["Month"])
                  if len(heavy) else f"No month above {HEAVY_MM} mm")
        elif choice == "3":
            compare_and_plot(df)
        elif choice == "4":
            trend_plot(df)
        elif choice == "5":
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
