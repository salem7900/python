import importlib
import sys

REQUIRED: dict[str, str] = {
    "pandas": "Data manipulation",
    "numpy": "Numerical computation",
    "matplotlib": "Visualization",
}


def check_dependencies() -> list[str]:
    """Controlla se i pacchetti sono stati installati e
    ritorna quelli mancanti in missing"""
    missing: list[str] = []

    print("Checking dependencies:")
    for name, description in REQUIRED.items():
        try:
            module = importlib.import_module(name)
            version = getattr(module, "__version__", "unknown")
            print(f"[OK] {name} ({version}) - {description} ready")
        except ImportError:
            print(f"[MISSING] {name} - {description}")
            missing.append(name)

    return missing


def analyze_data() -> None:
    """Genera 1000 numeri, li mette in un DataFrame
    e genera un istogramma."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    print("\nAnalyzing Matrix data...")
    """loc = media dei numeri, la media sarà vicina allo 0,
    scale = deviazione standard, quanto i numeri si allontanano dalla media,
    size = quantità dei numeri"""
    np.random.seed(42)
    data = np.random.normal(loc=0, scale=1, size=1000)
    df = pd.DataFrame({"signal": data})
    print(f"Processing {len(df)} data points...")
    print("Generating visualization...\n\n")

    """ plt.hist crea un istogramma con i numeri generati,
    bins è il numero di 'colonne' nella rappresentazione grafica"""
    plt.hist(df["signal"], bins=30)
    plt.savefig("matrix_analysis.png")
    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")


def main() -> None:
    print("LOADING STATUS: Loading programs...\n")
    missing = check_dependencies()

    if missing:
        print("\nMissing dependencies:", ", ".join(missing))
        print("Install with pip:    pip install -r requirements.txt")
        print("Install with Poetry: poetry install")
        sys.exit(1)

    analyze_data()


if __name__ == "__main__":
    main()
