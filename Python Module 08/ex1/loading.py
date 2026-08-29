#!/usr/bin/env python3
import sys
import importlib
import importlib.util
from importlib import metadata
from types import ModuleType
from typing import Dict, Optional, Tuple

# Packages required for the analysis itself.
REQUIRED_PACKAGES: Dict[str, str] = {
    "pandas": "Data manipulation",
    "numpy": "Numerical computation",
    "matplotlib": "Visualization",
}

# Packages that are nice to have but not mandatory (e.g. to fetch real data from an API instead of simulating it with numpy).
OPTIONAL_PACKAGES: Dict[str, str] = {
    "requests": "Network access",
}

OUTPUT_FILE = "matrix_analysis.png"
SAMPLE_SIZE = 1000


def get_version(package_name: str) -> Optional[str]:
    """Return the installed version of a package, or None if unknown."""
    try:
        return metadata.version(package_name)
    except metadata.PackageNotFoundError:
        return None


def load_module(module_name: str) -> Optional[ModuleType]:
    """Importa il modulo solo se esiste, altrimenti restituisce None
    """
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        return None
    return importlib.import_module(module_name)


def check_dependencies() -> Tuple[Dict[str, ModuleType], bool]:
    """Printa lo status di ogni pacchetto(richiesti + opzionali) dopo aver usato le due funzioni sopra.
    """
    print("Checking dependencies:")
    loaded: Dict[str, ModuleType] = {}
    all_required_ok = True

    all_packages = {**REQUIRED_PACKAGES, **OPTIONAL_PACKAGES}
    for name, description in all_packages.items():
        module = load_module(name)
        version = get_version(name)

        if module is not None:
            loaded[name] = module
            version_str = version if version else "unknown"
            print(f"  [OK] {name} ({version_str}) - "
                  f"{description} ready")
        else:
            print(f"  [MISSING] {name} - {description} not available")
            if name in REQUIRED_PACKAGES:
                all_required_ok = False

    print()
    return loaded, all_required_ok


def print_installation_instructions() -> None:
    """Explain how to install the missing dependencies."""
    required_list = " ".join(REQUIRED_PACKAGES)

    print("MISSING DEPENDENCIES DETECTED")
    print()
    print("This program cannot run the Matrix analysis without the")
    print("packages listed above as [MISSING].")
    print()
    print("--- Option 1: Install with pip ---")
    print("  pip install -r requirements.txt")
    print(f"  # or directly: pip install {required_list}")
    print()
    print("--- Option 2: Install with Poetry ---")
    print("  poetry install")
    print("  poetry run python loading.py")
    print()
    print("Then run this program again:")
    print("  python3 loading.py")


def compare_pip_poetry(loaded: Dict[str, ModuleType]) -> None:
    """Print a short comparison between pip and Poetry workflows."""
    print("--- pip vs Poetry ---")
    print("pip:")
    print("  - Reads a flat requirements.txt file.")
    print("  - No built-in lock file; versions can drift between")
    print("    installs unless pins are managed manually.")
    print("  - Installs into whatever environment is active.")
    print()
    print("Poetry:")
    print("  - Reads pyproject.toml for dependency constraints.")
    print("  - Resolves and freezes exact versions in poetry.lock,")
    print("    so every install is reproducible.")
    print("  - Manages its own virtual environment automatically.")
    print()

    print("Installed package versions (this environment):")
    all_names = {**REQUIRED_PACKAGES, **OPTIONAL_PACKAGES}
    for name in all_names:
        version = get_version(name)
        status = version if version else "not installed"
        print(f"  {name}: {status}")
    print()


def generate_matrix_data(
    np_module: ModuleType, size: int
) -> "object":
    """np_module.random.default_rng(seed=42) crea un generatore di numeri casuali.
    Il seed=42 fa sì che i numeri "casuali" siano sempre gli stessi ad ogni esecuzione (utile per test riproducibili).
    """
    rng = np_module.random.default_rng(seed=42)

    # "Digital rain" intensity per data point.
    signal = rng.normal(loc=50.0, scale=15.0, size=size)
    signal = np_module.clip(signal, 0, 100)

    # Derived "anomaly score": how far a point is from the mean,
    # plus a bit of independent noise (simulated glitches).
    noise = rng.normal(loc=0.0, scale=5.0, size=size)
    anomaly_score = np_module.abs(signal - signal.mean()) + noise

    timestamps = np_module.arange(size)

    return {
        "timestamp": timestamps,
        "signal": signal,
        "anomaly_score": anomaly_score,
    }


def analyze_and_plot(
    pd_module: ModuleType,
    plt_module: ModuleType,
    raw_data: "object",
    size: int,
) -> None:
    """pd_module.DataFrame(raw_data) trasforma il dizionario di numeri in una tabella pandas.
    .describe() calcola statistiche automatiche: media, minimo, massimo, percentili, ecc.
    plt_module.subplots(2, 1, ...) crea una figura con 2 grafici impilati:
    sopra il segnale nel tempo (linea), sotto la distribuzione delle anomalie (istogramma).
    figure.savefig("matrix_analysis.png") salva il grafico su disco come immagine."""
    print("Analyzing Matrix data...")
    print(f"Processing {size} data points...")

    dataframe = pd_module.DataFrame(raw_data)

    summary = dataframe[["signal", "anomaly_score"]].describe()
    print()
    print("Summary statistics:")
    print(summary)
    print()

    print("Generating visualization...")
    figure, axes = plt_module.subplots(2, 1, figsize=(10, 8))

    axes[0].plot(
        dataframe["timestamp"], dataframe["signal"],
        color="green", linewidth=0.7,
    )
    axes[0].set_title("Matrix Signal Over Time")
    axes[0].set_xlabel("Timestamp")
    axes[0].set_ylabel("Signal Intensity")

    axes[1].hist(
        dataframe["anomaly_score"], bins=30, color="darkgreen",
    )
    axes[1].set_title("Anomaly Score Distribution")
    axes[1].set_xlabel("Anomaly Score")
    axes[1].set_ylabel("Frequency")

    figure.tight_layout()
    figure.savefig(OUTPUT_FILE)
    plt_module.close(figure)

    print()
    print("Analysis complete!")
    print(f"Results saved to: {OUTPUT_FILE}")


def main() -> int:
    print("LOADING STATUS: Loading programs...")
    print()

    loaded, all_required_ok = check_dependencies()
    compare_pip_poetry(loaded)

    if not all_required_ok:
        print_installation_instructions()
        return 1

    pd_module = loaded["pandas"]
    np_module = loaded["numpy"]
    matplotlib_module = loaded["matplotlib"]
    matplotlib_module.use("Agg")
    plt_module = load_module("matplotlib.pyplot")
    if plt_module is None:
        print("[MISSING] matplotlib.pyplot - Visualization not "
              "available")
        return 1

    raw_data = generate_matrix_data(np_module, SAMPLE_SIZE)
    analyze_and_plot(pd_module, plt_module, raw_data, SAMPLE_SIZE)

    return 0


"""Lancia main() solo se il file viene eseguito direttamente, e usa sys.exit() per restituire al
terminale il codice di uscita di main() (0 = tutto ok, 1 = errore/dipendenze mancanti)
— così script esterni o CI possono sapere se il programma è andato a buon fine."""
if __name__ == "__main__":
    sys.exit(main())
