import subprocess
import sys


def run_lint():
    """
    Runs Ruff to format and lint (with auto-fix) all Python files in the project.
    """
    print("Running Ruff Formatter...")
    format_cmd = ["uv", "run", "ruff", "format", "."]

    print("Running Ruff Linter (with --fix)...")
    lint_cmd = ["uv", "run", "ruff", "check", ".", "--fix"]

    try:
        # Run formatter
        subprocess.run(format_cmd, check=True)
        # Run linter
        subprocess.run(lint_cmd, check=True)
        print("Linting and formatting completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during linting/formatting: {e}")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("Error: 'uv' or 'ruff' not found. Make sure they are installed.")
        sys.exit(1)


if __name__ == "__main__":
    run_lint()
