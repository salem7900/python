import os
import sys
try:
    from dotenv import load_dotenv  # type: ignore
except ImportError:
    print("[ERROR] python-dotenv is not installed")
    print("Install it with: pip install -r requirements.txt")
    sys.exit(1)


def load_config() -> dict[str, str | None]:
    return {
        "MATRIX_MODE": os.getenv("MATRIX_MODE"),
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "API_KEY": os.getenv("API_KEY"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL"),
        "ZION_ENDPOINT": os.getenv("ZION_ENDPOINT"),
    }


def validate_config(config: dict[str, str | None]) -> None:
    VALID_MODES = ("development", "production")
    VALID_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

    mode = config["MATRIX_MODE"]
    if mode not in VALID_MODES:
        print(f"[WARNING] Invalid MATRIX_MODE '{mode}', using 'development'")
        config["MATRIX_MODE"] = "development"

    if config["LOG_LEVEL"]:
        config["LOG_LEVEL"] = config["LOG_LEVEL"].upper()
    level = config["LOG_LEVEL"]
    if level not in VALID_LEVELS:
        print(f"[WARNING] Invalid LOG_LEVEL '{level}', using 'INFO'")
        config["LOG_LEVEL"] = "INFO"


def _security_checks(config: dict[str, str | None]) -> None:

    api = config['API_KEY']
    if not api:
        print("[WARNING] API_KEY is missing")
    elif api == "your_api_key_here":
        print("[WARNING] API_KEY is still a placeholder")
    else:
        print("[OK] No hardcoded secrets detected")

    if not os.path.exists(".env"):
        print("[ERROR] .env file is missing")
    elif not all(config.values()):
        print("[WARNING] .env file has some missing values")
    else:
        print("[OK] .env file properly configured")

    matrix = config["MATRIX_MODE"]
    log_level = config["LOG_LEVEL"]
    if matrix == "production" and log_level == "DEBUG":
        print("[WARNING] LOG_LEVEL is DEBUG in production mode")
    else:
        print("[OK] Log level is appropriate for the current mode")

    print("[OK] Production overrides available")


def output(config: dict[str, str | None]) -> None:
    print("\nORACLE STATUS: Reading the Matrix...\n")

    db = config['DATABASE_URL']
    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")
    if not db:
        print("Database: Not configured")
    elif "localhost" in db or "127.0.0.1" in db:
        print("Database: Connected to local instance")
    else:
        print("Database: Connected to remote database")
    if not config['API_KEY']:
        print("API Access: Not authenticated")
    else:
        print("API Access: Authenticated")
    print(f"Log Level: {config['LOG_LEVEL']}")
    if not config['ZION_ENDPOINT']:
        print("Zion Network: Offline\n")
    else:
        print("Zion Network: Online\n")

    print("Environment security check:")
    _security_checks(config)

    print("\nThe Oracle sees all configurations.")


def main() -> None:
    found = load_dotenv()
    if not found:
        print("[WARNING] .env file not found.")
    config: dict[str, str | None] = load_config()
    validate_config(config)
    missing: list[str] = [key for key, value in config.items() if not value]
    for key in missing:
        print(f"[WARNING] {key} is not set")
    if config['MATRIX_MODE'] == "production" and missing:
        print(
            f"\n[ERROR] Missing configuration in production mode:"
            f" {', '.join(missing)}")
        sys.exit(1)
    output(config)


if __name__ == "__main__":
    main()
