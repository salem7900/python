#!/usr/bin/env python3
import sys
import os
import site


def get_virtual_env_name() -> str:
    """os.path.basename() restituisce l'ultima parte del percorso, quindi la cartella in cui c'è il venv
    os.environ è un dizionario che contiene tutte le variabili d'ambiente del sistema
    usando .get restuisci il contenuto della variabile o None se non c'è la variabile """
    venv_path = os.environ.get("VIRTUAL_ENV")
    if venv_path:
        return os.path.basename(os.path.normpath(venv_path))
    return os.path.basename(os.path.normpath(sys.prefix))


def is_virtual_env() -> bool:
    """sys.base_prefix punta alla cartella di installazione di python
        sys.prefix punta al venv se presente
        sys.real_prefix è creato solo con virtualenv
        VIRTUAL_ENV è una variabile creata quando si usa source matrix_env/bin/activate"""
    base_prefix_differs = (
            hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )
    has_real_prefix = hasattr(sys, "real_prefix")
    has_env_var = os.environ.get("VIRTUAL_ENV") is not None

    return base_prefix_differs or has_real_prefix or has_env_var


def get_site_packages_path() -> str:
    """site ritorna la cartella su cui python installa quando fai pip install"""
    site_packages = site.getsitepackages()
    if site_packages:
        return site_packages[0]
    return site.getusersitepackages()


def print_outside_matrix() -> None:
    print("MATRIX STATUS: You're still plugged in")
    print()
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print(f"Global package location: {get_site_packages_path()}")
    print()
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print("To enter the construct, run:")
    print()
    print("    python3 -m venv matrix_env")
    print("    source matrix_env/bin/activate      # On Unix")
    print("    matrix_env\\Scripts\\activate         # On Windows")
    print()
    print("Then run this program again.")


def print_inside_matrix() -> None:
    env_name = get_virtual_env_name()
    env_path = os.environ.get("VIRTUAL_ENV", sys.prefix)

    print("MATRIX STATUS: Welcome to the construct")
    print()
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {env_name}")
    print(f"Environment Path: {env_path}")
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting the global system.")
    print()
    print(f"Package installation path: {get_site_packages_path()}")


def main() -> None:
    if is_virtual_env():
        print_inside_matrix()
    else:
        print_outside_matrix()


if __name__ == "__main__":
    main()
