import subprocess
import sys
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent
    print("Starting Unified Dashboard (Local)...")
    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(root / "railway_app.py"), "--server.port", "8501"],
            cwd=str(root),
            check=True
        )
    except KeyboardInterrupt:
        print("\nStopped.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
