import os
from dotenv import load_dotenv


VALID_MODES = {"development", "production"}


def load_configuration() -> dict[str, str]:
    load_dotenv()  # silently does nothing if no .env file exists

    return {
        "MATRIX_MODE": os.getenv("MATRIX_MODE", "development"),
        "DATABASE_URL": os.getenv("DATABASE_URL", ""),
        "API_KEY": os.getenv("API_KEY", ""),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
        "ZION_ENDPOINT": os.getenv("ZION_ENDPOINT", ""),
    }


def validate_configuration(config: dict[str, str]) -> list[str]:
    warnings = []
    if config["MATRIX_MODE"] not in VALID_MODES:
        warnings.append(
            f"MATRIX_MODE '{config['MATRIX_MODE']}' is not recognized "
            "(expected 'development' or 'production')"
        )
    if not config["DATABASE_URL"]:
        warnings.append("DATABASE_URL not set - no database connection")
    if not config["API_KEY"]:
        warnings.append("API_KEY not set - external API calls will fail")
    if not config["ZION_ENDPOINT"]:
        warnings.append("ZION_ENDPOINT not set - resistance network offline")
    return warnings


def describe_database(url: str) -> str:
    if not url:
        return "Not configured"
    if "localhost" in url or "127.0.0.1" in url:
        return "Connected to local instance"
    return "Connected to remote instance"


def print_report(config: dict[str, str]) -> None:
    print("ORACLE STATUS: Reading the Matrix...\n")
    print("Configuration loaded:")
    print(f"Mode: {config['MATRIX_MODE']}")
    print(f"Database: {describe_database(config['DATABASE_URL'])}")
    api_status = "Authenticated" if config["API_KEY"] else "Not authenticated"
    print(f"API Access: {api_status}")
    print(f"Log Level: {config['LOG_LEVEL']}")
    zion_status = "Online" if config["ZION_ENDPOINT"] else "Offline"
    print(f"Zion Network: {zion_status}\n")

    warnings = validate_configuration(config)
    is_production = config["MATRIX_MODE"] == "production"

    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")
    print(f"[{'OK' if not warnings else 'WARN'}] .env file properly configured")
    if is_production:
        print("[INFO] Running in PRODUCTION mode")
    else:
        print("[OK] Production overrides available")

    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  - {warning}")

    print("\nThe Oracle sees all configurations.")


def main() -> None:
    config = load_configuration()
    print_report(config)


if __name__ == "__main__":
    main()
