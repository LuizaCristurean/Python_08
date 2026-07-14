import os
import sys
import site


def check_environment() -> None:
    is_venv = sys.prefix != sys.base_prefix
    packages_paths = site.getsitepackages()

    if not is_venv:
        print("MATRIX STATUS: You're still plugged in\n")
        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: None detected")
        print("\nWARNING: You're in the global environment!")
        print("The machine can see everything you install.\n")
        print("To enter the construct, run:")
        print("python3 -m venv matrix_env")
        print("source matrix_env/bin/activate # On Unix\n")
        print("Then run this program again.")
    else:
        print("MATRIX STATUS: Welcome to the construct\n")
        print(f"Current Python: {sys.executable}")
        venv_name = os.path.basename(sys.prefix)
        print(f"Virtual Environment: {venv_name}")
        print(f"Environment Path: {sys.prefix}")
        print("\nSUCCESS: You're in an isolated environment!")
        print(
            "Safe to install packages without affecting the global system.\n")
        print("Package installation path: ")
        print(packages_paths[0])


if __name__ == "__main__":
    check_environment()
