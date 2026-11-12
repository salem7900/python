import os
import site
import sys


def is_virtual_env() -> bool:
    return sys.prefix != sys.base_prefix


def venv_display() -> None:
    env_path = sys.prefix
    env_name = os.path.basename(env_path)

    output: str = (
        "\nMATRIX STATUS: Welcome to the construct\n\n"
        + f"Current Python: {sys.executable}\n"
        + f"Virtual Environment: {env_name}\n"
        + f"Environment Path: {env_path}\n\n"
        + "SUCCESS: You're in an isolated environment!\n"
        + "Safe to install packages without affecting\n"
        + "the global system.\n\n"
        + "Package installation path:\n"
        + f"{site.getsitepackages()[0]}"
    )
    print(output)


def no_venv_display() -> None:
    output: str = (
        "\nMATRIX STATUS: You're still plugged in\n\n"
        + f"Current Python: {sys.executable}\n"
        + "Virtual Environment: None detected\n\n"
        + "WARNING: You're in the global environment!\n"
        + "The machines can see everything you install.\n\n"
        + "To enter the construct, run:\n"
        + "python3 -m venv matrix_env\n"
        + "source matrix_env/bin/activate # On Unix\n"
        + "matrix_env\\Scripts\\activate # On Windows\n\n"
        + "Then run this program again."
    )
    print(output)


def main() -> None:
    if is_virtual_env():
        venv_display()
    else:
        no_venv_display()


if __name__ == "__main__":
    main()
