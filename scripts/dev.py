import os
import subprocess
import sys
import argparse
import dotenv


def run_dev_server():
    """
    Invokes the development server using uv and uvicorn.
    """
    parser = argparse.ArgumentParser(description="Run the development server.")
    parser.add_argument("--staging", action="store_true", help="Run in staging mode (load .env.stage)")
    args = parser.parse_args()

    if args.staging:
        env_file = ".env.stage"
        os.environ["ENV"] = "staging"
    else:
        env_file = ".env.dev"
        os.environ["ENV"] = "development"

    print(f"Loading environment from {env_file}...")
    dotenv.load_dotenv(dotenv_path=env_file, override=True)

    command = ["uv", "run", "uvicorn", "app.main:app", "--reload", "--port", os.getenv("PORT", "5000")]

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
