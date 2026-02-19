import streamlit as st
import sys
import os
from pathlib import Path

# Calculate the path to the actual app
current_dir = Path(__file__).parent.resolve()
root_dir = current_dir.parent
target_dir = root_dir / "googlesearch"
target_script = target_dir / "app_streamlit.py"

# Add the target directory to sys.path so imports work
if str(target_dir) not in sys.path:
    sys.path.append(str(target_dir))

# Change working directory to the target directory to ensure relative file operations work
os.chdir(target_dir)

# Execute the script
try:
    with open(target_script, "r", encoding="utf-8") as f:
        code = f.read()
        exec(code, globals())
except Exception as e:
    st.error(f"Error running app: {e}")
    import traceback
    st.code(traceback.format_exc())
