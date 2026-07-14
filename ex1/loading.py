import sys
from importlib.metadata import PackageNotFoundError, version
from typing import Any


REQUIRED_PACKAGES = ["pandas", "numpy", "matplotlib"]
OPTIONAL_PACKAGES = ["requests"]
PACKAGE_DESCRIPTIONS = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
    "matplotlib": "Visualization ready",
    "requests": "Network access ready",
}


def check_dependencies() -> dict[str, str | None]:
    status: dict[str, str | None] = {}
    for pkg in REQUIRED_PACKAGES + OPTIONAL_PACKAGES:
        try:
            status[pkg] = version(pkg)
        except PackageNotFoundError:
            status[pkg] = None
    return status


def print_dependency_report(status: dict[str, str | None]) -> None:
    print("Checking dependencies:")
    for pkg, ver in status.items():
        if ver is not None:
            desc = PACKAGE_DESCRIPTIONS.get(pkg, "")
            print(f"[OK] {pkg} ({ver}) - {desc}")
        else:
            print(f"[MISSING] {pkg} - not installed")


def missing_required(status: dict[str, str | None]) -> list[str]:
    return [pkg for pkg in REQUIRED_PACKAGES if status[pkg] is None]


def show_install_instructions(missing: list[str]) -> None:
    print("\nMissing required dependencies:", ", ".join(missing))
    print("\nInstall with pip:")
    print("    pip install -r requirements.txt")
    print("\nOr install with Poetry (locks exact versions for everyone):")
    print("    poetry install")
    print("    poetry run python loading.py")


def generate_matrix_data(n_points: int = 1000) -> tuple[Any, Any]:

    import numpy as np

    rng = np.random.default_rng(seed=42)
    timestamps = np.arange(n_points)
    # A noisy signal centered at 50, like a fluctuating power reading.
    signal = rng.normal(loc=50.0, scale=15.0, size=n_points)
    return timestamps, signal


def analyze_data(timestamps: Any, signal: Any) -> Any:
    import pandas as pd

    df = pd.DataFrame({"timestamp": timestamps, "signal": signal})
    return df


def visualize(df: Any, output_path: str = "matrix_analysis.png") -> None:

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 5))
    plt.plot(df["timestamp"], df["signal"])
    plt.title("Matrix Data Stream")
    plt.xlabel("Time")
    plt.ylabel("Signal Strength")
    plt.savefig(output_path)
    plt.close()


def main() -> None:
    print("LOADING STATUS: Loading programs...\n")

    status = check_dependencies()
    print_dependency_report(status)

    missing = missing_required(status)
    if missing:
        show_install_instructions(missing)
        sys.exit(1)

    print("\nAnalyzing Matrix data...")
    timestamps, signal = generate_matrix_data(1000)
    print(f"Processing {len(timestamps)} data points...")

    df = analyze_data(timestamps, signal)

    print("Generating visualization...")
    visualize(df)

    print("\nAnalysis complete!")
    print("Results saved to: matrix_analysis.png")


if __name__ == "__main__":
    main()
