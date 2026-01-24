import subprocess
import sys


def run_dev_server():
    """
    Invokes the development server using uv and uvicorn.
    """
    command = ["uv", "run", "uvicorn", "app.main:app", "--reload", "--port", "8080"]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting the development server: {e}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C
        sys.exit(0)


if __name__ == "__main__":
    run_dev_server()
