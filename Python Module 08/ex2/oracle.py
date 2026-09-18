#!/usr/bin/env python3
"""
Rule of thumb applied throughout this file: environment variables
that are already set in the shell always win over the .env file, and
the .env file always wins over hardcoded defaults. Real secrets are
never written into this script.
"""

import os
import sys
from typing import Callable, Dict, Optional, Tuple

try:
    from dotenv import load_dotenv as _load_dotenv
    DOTENV_LOAD: Optional[Callable[..., bool]] = _load_dotenv
except ImportError:
    DOTENV_LOAD = None

REQUIRED_VARS = (
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
)

# Fallback values used only in development mode, and only when a
# variable is missing from both the environment and the .env file.
DEVELOPMENT_DEFAULTS: Dict[str, str] = {
    "MATRIX_MODE": "development",
    "DATABASE_URL": "sqlite:///local_matrix.db",
    "API_KEY": "",
    "LOG_LEVEL": "DEBUG",
    "ZION_ENDPOINT": "",
}

ENV_FILE = ".env"
ENV_EXAMPLE_FILE = ".env.example"
GITIGNORE_FILE = ".gitignore"


def mask_secret(value: str, keep: int = 4) -> str:
    """Sostituisce il valore di API_KEY con asterischi per nasconderlo."""
    if not value:
        return "(not set)"
    if len(value) <= keep:
        return "*" * len(value)
    return value[:keep] + "*" * (len(value) - keep)


def is_local_database(url: str) -> bool:
    """Traduce un URL tecnico in un messaggio umano da stampare per verificare
    in quale ambiente si sta usando il programma, se in sviluppo o in produzione.
    -"Demonstrates different configuration for development/production. it must be visible in the output"
    """
    if not url:
        return False
    lowered = url.lower()
    local_markers = ("sqlite", "localhost", "127.0.0.1")
    return any(marker in lowered for marker in local_markers)


def snapshot_env(names: Tuple[str, ...]) -> Dict[str, Optional[str]]:
    """Return a copy of the current values of the given env vars."""
    return {name: os.environ.get(name) for name in names}


def build_config(
    pre_env: Dict[str, Optional[str]],
) -> Dict[str, Dict[str, str]]:
    """Controlla da dove viene il valore:
        1. Environment variable set before running the program
        2. Value found in the .env file
        3. Development-only hardcoded default
        4. Missing entirely
    """
    mode = os.environ.get("MATRIX_MODE", "development")
    is_dev = mode != "production"

    config: Dict[str, Dict[str, str]] = {}
    for name in REQUIRED_VARS:
        current = os.environ.get(name)

        if pre_env.get(name) is not None:
            source = "environment variable (override)"
        elif current is not None:
            source = ".env file"
        elif is_dev and DEVELOPMENT_DEFAULTS.get(name):
            source = "development default"
            current = DEVELOPMENT_DEFAULTS[name]
        else:
            source = "missing"
            current = ""

        config[name] = {"value": current or "", "source": source}

    return config


def print_configuration(config: Dict[str, Dict[str, str]]) -> None:
    """Print the resolved configuration in a human-friendly form."""
    mode = config["MATRIX_MODE"]["value"] or "development"
    db_url = config["DATABASE_URL"]["value"]
    api_key = config["API_KEY"]["value"]
    log_level = config["LOG_LEVEL"]["value"] or "INFO"
    zion_endpoint = config["ZION_ENDPOINT"]["value"]

    print("Configuration loaded:")
    print(f"  Mode: {mode}")

    if not db_url:
        print("  Database: NOT CONFIGURED (missing DATABASE_URL)")
    elif is_local_database(db_url):
        print("  Database: Connected to local instance")
    else:
        print("  Database: Connected to remote instance")

    if not api_key:
        print("  API Access: Not authenticated (missing API_KEY)")
    else:
        print(f"  API Access: Authenticated ({mask_secret(api_key)})")

    print(f"  Log Level: {log_level}")

    if not zion_endpoint:
        print("  Zion Network: Offline (missing ZION_ENDPOINT)")
    else:
        print(f"  Zion Network: Online ({zion_endpoint})")

    print()
    print("Configuration sources:")
    for name in REQUIRED_VARS:
        print(f"  {name}: {config[name]['source']}")
    print()

    if mode == "production" and log_level.upper() == "DEBUG":
        print("[WARNING] DEBUG log level in production can leak "
              "sensitive data into logs.")
        print()


def check_no_hardcoded_secrets(config: Dict[str, Dict[str, str]]) -> bool:
    """Controlla che la API_KEY non è scritta nel programma ma è presa da .env.
    La API_KEY deve rimanere segreta.
    """
    try:
        with open(__file__, "r", encoding="utf-8") as source_file:
            source_code = source_file.read()
    except OSError:
        # If we can't even read our own file, fail safe: don't claim
        # the check passed.
        return False

    external_sources = ("environment variable (override)", ".env file")
    api_key = config["API_KEY"]["value"]
    api_key_source = config["API_KEY"]["source"]
    if (
        api_key
        and api_key_source in external_sources
        and api_key in source_code
    ):
        return False

    return True


def check_env_file_configured() -> bool:
    """Controlla che il vero file .env sia escluso da .gitignore..
    """
    if not os.path.isfile(GITIGNORE_FILE):
        return False

    try:
        with open(GITIGNORE_FILE, "r", encoding="utf-8") as gitignore:
            lines = [line.strip() for line in gitignore.readlines()]
    except OSError:
        return False

    return ENV_FILE in lines


def check_production_overrides(pre_env: Dict[str, Optional[str]]) -> bool:
    """Controlla che i valori impostati prima di load_dotenv() non siano sovrascritti.
    """
    for name, original_value in pre_env.items():
        if original_value is not None:
            if os.environ.get(name) != original_value:
                return False
    return True


def print_security_check(
    pre_env: Dict[str, Optional[str]],
    config: Dict[str, Dict[str, str]],
) -> None:
    """Run and print the environment security checks."""
    print("Environment security check:")

    secrets_ok = check_no_hardcoded_secrets(config)
    status = "[OK]" if secrets_ok else "[FAIL]"
    print(f"  {status} No hardcoded secrets detected")

    env_file_ok = check_env_file_configured()
    status = "[OK]" if env_file_ok else "[FAIL]"
    print(f"  {status} .env file properly configured (ignored by git)")

    overrides_ok = check_production_overrides(pre_env)
    status = "[OK]" if overrides_ok else "[FAIL]"
    print(f"  {status} Production overrides available")
    print()


def main() -> int:
    print("ORACLE STATUS: Reading the Matrix...")
    print()

    # Salva i valori delle 5 variabili prima di leggere il file .env
    pre_env = snapshot_env(REQUIRED_VARS)

    # Legge il file .env riga per riga
    # e modifica solo le variabili che non esistono già (override=FALSE)
    _load_dotenv(dotenv_path=ENV_FILE, override=False)

    config = build_config(pre_env)

    missing = [name for name in REQUIRED_VARS
               if config[name]["source"] == "missing"]
    mode = config["MATRIX_MODE"]["value"] or "development"

    if missing:
        print("[WARNING] Missing configuration detected:")
        for name in missing:
            print(f"  - {name} is not set (no env var, no .env entry)")
        print()
        print("Copy .env.example to .env and fill in real values, "
              "or export the variables in your shell.")
        print()

    # Ferma il programma se mancano dati critici
    if mode == "production" and (
        not config["DATABASE_URL"]["value"]
        or not config["API_KEY"]["value"]
    ):
        print("[ERROR] Production mode requires DATABASE_URL and "
              "API_KEY to be set. Refusing to continue.")
        return 1

    print_configuration(config)
    print_security_check(pre_env, config)

    print("The Oracle sees all configurations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""
#!/usr/bin/env python3
"""
oracle.py - The Oracle

Reads application configuration from environment variables, using a
.env file (via python-dotenv) to provide development defaults.

Rule of thumb applied throughout this file: environment variables
that are already set in the shell always win over the .env file, and
the .env file always wins over hardcoded defaults. Real secrets are
never written into this script.

Authorized: os, sys, python-dotenv, file operations.
"""

import os
import sys
from typing import Callable, Dict, Optional, Tuple

# python-dotenv is required by this exercise, but the program must
# never crash with a raw traceback if it happens to be missing from
# the current environment (e.g. dependencies not installed yet). We
# degrade gracefully instead: configuration still works from real
# environment variables, we just skip reading the .env file and warn
# the user how to fix it.
try:
    from dotenv import load_dotenv as _load_dotenv
    DOTENV_LOAD: Optional[Callable[..., bool]] = _load_dotenv
except ImportError:
    DOTENV_LOAD = None

REQUIRED_VARS = (
    "MATRIX_MODE",
    "DATABASE_URL",
    "API_KEY",
    "LOG_LEVEL",
    "ZION_ENDPOINT",
)

# Fallback values used only in development mode, and only when a
# variable is missing from both the environment and the .env file.
DEVELOPMENT_DEFAULTS: Dict[str, str] = {
    "MATRIX_MODE": "development",
    "DATABASE_URL": "sqlite:///local_matrix.db",
    "API_KEY": "",
    "LOG_LEVEL": "DEBUG",
    "ZION_ENDPOINT": "",
}

ENV_FILE = ".env"
ENV_EXAMPLE_FILE = ".env.example"
GITIGNORE_FILE = ".gitignore"


def mask_secret(value: str, keep: int = 4) -> str:
    """Mask a secret, keeping only its first few characters visible."""
    if not value:
        return "(not set)"
    if len(value) <= keep:
        return "*" * len(value)
    return value[:keep] + "*" * (len(value) - keep)


def is_local_database(url: str) -> bool:
    """Heuristically decide whether a DATABASE_URL points to a local
    resource (sqlite file, localhost, 127.0.0.1) rather than a remote
    server.
    """
    if not url:
        return False
    lowered = url.lower()
    local_markers = ("sqlite", "localhost", "127.0.0.1")
    return any(marker in lowered for marker in local_markers)


def snapshot_env(names: Tuple[str, ...]) -> Dict[str, Optional[str]]:
    """Return a copy of the current values of the given env vars."""
    return {name: os.environ.get(name) for name in names}


def build_config(
    pre_env: Dict[str, Optional[str]],
) -> Dict[str, Dict[str, str]]:
    """Resolve every required variable and record where it came from.

    Precedence (handled automatically by load_dotenv, called with its
    default override=False before this function runs):
        1. Environment variable set before running the program
        2. Value found in the .env file
        3. Development-only hardcoded default
        4. Missing entirely
    """
    mode = os.environ.get("MATRIX_MODE", "development")
    is_dev = mode != "production"

    config: Dict[str, Dict[str, str]] = {}
    for name in REQUIRED_VARS:
        current = os.environ.get(name)

        if pre_env.get(name) is not None:
            source = "environment variable (override)"
        elif current is not None:
            source = ".env file"
        elif is_dev and DEVELOPMENT_DEFAULTS.get(name):
            source = "development default"
            current = DEVELOPMENT_DEFAULTS[name]
        else:
            source = "missing"
            current = ""

        config[name] = {"value": current or "", "source": source}

    return config


def print_configuration(config: Dict[str, Dict[str, str]]) -> None:
    """Print the resolved configuration in a human-friendly form."""
    mode = config["MATRIX_MODE"]["value"] or "development"
    db_url = config["DATABASE_URL"]["value"]
    api_key = config["API_KEY"]["value"]
    log_level = config["LOG_LEVEL"]["value"] or "INFO"
    zion_endpoint = config["ZION_ENDPOINT"]["value"]

    print("Configuration loaded:")
    print(f"  Mode: {mode}")

    if not db_url:
        print("  Database: NOT CONFIGURED (missing DATABASE_URL)")
    elif is_local_database(db_url):
        print("  Database: Connected to local instance")
    else:
        print("  Database: Connected to remote instance")

    if not api_key:
        print("  API Access: Not authenticated (missing API_KEY)")
    else:
        print(f"  API Access: Authenticated ({mask_secret(api_key)})")

    print(f"  Log Level: {log_level}")

    if not zion_endpoint:
        print("  Zion Network: Offline (missing ZION_ENDPOINT)")
    else:
        print(f"  Zion Network: Online ({zion_endpoint})")

    print()
    print("Configuration sources:")
    for name in REQUIRED_VARS:
        print(f"  {name}: {config[name]['source']}")
    print()

    if mode == "production" and log_level.upper() == "DEBUG":
        print("[WARNING] DEBUG log level in production can leak "
              "sensitive data into logs.")
        print()


def check_no_hardcoded_secrets(config: Dict[str, Dict[str, str]]) -> bool:
    """Verify this very script does not contain any resolved secret.

    Reads oracle.py's own source and checks that the real API_KEY
    coming from the environment or the .env file (as opposed to our
    own intentional, non-secret development defaults) does not
    appear there as literal text. That would indicate someone pasted
    a real secret directly into the code instead of loading it from
    the environment. DATABASE_URL is intentionally not checked here:
    unlike an API key, a bare connection string is not always
    sensitive (e.g. a local sqlite path), and development defaults
    for it may legitimately match values also used in .env.example.
    """
    try:
        with open(__file__, "r", encoding="utf-8") as source_file:
            source_code = source_file.read()
    except OSError:
        # If we can't even read our own file, fail safe: don't claim
        # the check passed.
        return False

    external_sources = ("environment variable (override)", ".env file")
    api_key = config["API_KEY"]["value"]
    api_key_source = config["API_KEY"]["source"]
    if (
        api_key
        and api_key_source in external_sources
        and api_key in source_code
    ):
        return False

    return True


def check_env_file_configured() -> bool:
    """Verify .env is excluded from version control via .gitignore.

    A well-configured project ships a .env.example template (safe to
    commit) but ignores the real .env file (which may hold real
    secrets) via .gitignore.
    """
    if not os.path.isfile(GITIGNORE_FILE):
        return False

    try:
        with open(GITIGNORE_FILE, "r", encoding="utf-8") as gitignore:
            lines = [line.strip() for line in gitignore.readlines()]
    except OSError:
        return False

    return ENV_FILE in lines


def check_production_overrides(pre_env: Dict[str, Optional[str]]) -> bool:
    """Verify env vars set before load_dotenv() were not overwritten.

    load_dotenv() is called with its default override=False, so any
    variable already present in the environment must keep its
    original value after loading the .env file. This confirms
    production deployments (which set real env vars, no .env file)
    can safely override development defaults.
    """
    for name, original_value in pre_env.items():
        if original_value is not None:
            if os.environ.get(name) != original_value:
                return False
    return True


def print_security_check(
    pre_env: Dict[str, Optional[str]],
    config: Dict[str, Dict[str, str]],
) -> None:
    """Run and print the environment security checks."""
    print("Environment security check:")

    secrets_ok = check_no_hardcoded_secrets(config)
    status = "[OK]" if secrets_ok else "[FAIL]"
    print(f"  {status} No hardcoded secrets detected")

    env_file_ok = check_env_file_configured()
    status = "[OK]" if env_file_ok else "[FAIL]"
    print(f"  {status} .env file properly configured (ignored by git)")

    overrides_ok = check_production_overrides(pre_env)
    status = "[OK]" if overrides_ok else "[FAIL]"
    print(f"  {status} Production overrides available")
    print()


def main() -> int:
    """Entry point."""
    print("ORACLE STATUS: Reading the Matrix...")
    print()

    # Snapshot the environment *before* touching the .env file, so we
    # can later prove which variables were overridden externally.
    pre_env = snapshot_env(REQUIRED_VARS)

    if DOTENV_LOAD is not None:
        # override=False (the default): variables already set in the
        # environment are never replaced by values from the .env
        # file.
        DOTENV_LOAD(dotenv_path=ENV_FILE, override=False)
    else:
        print("[WARNING] python-dotenv is not installed - the .env "
              "file will be ignored.")
        print("  Install it with: pip install -r requirements.txt")
        print("  Configuration will still work from real environment "
              "variables.")
        print()

    config = build_config(pre_env)

    missing = [name for name in REQUIRED_VARS
               if config[name]["source"] == "missing"]
    mode = config["MATRIX_MODE"]["value"] or "development"

    if missing:
        print("[WARNING] Missing configuration detected:")
        for name in missing:
            print(f"  - {name} is not set (no env var, no .env entry)")
        print()
        print("Copy .env.example to .env and fill in real values, "
              "or export the variables in your shell.")
        print()

    if mode == "production" and (
        not config["DATABASE_URL"]["value"]
        or not config["API_KEY"]["value"]
    ):
        print("[ERROR] Production mode requires DATABASE_URL and "
              "API_KEY to be set. Refusing to continue.")
        return 1

    print_configuration(config)
    print_security_check(pre_env, config)

    print("The Oracle sees all configurations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
"""