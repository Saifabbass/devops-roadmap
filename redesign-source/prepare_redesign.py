"""Rebuild current presentation and guided lessons without restoring the old baseline."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parents[1] / "tools" / "build_fieldbook.py"), run_name="__main__")
