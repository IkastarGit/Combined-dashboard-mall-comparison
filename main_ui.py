"""
Combined Dashboard - Main UI
Run: streamlit run main_ui.py --server.port 8501
Apps start automatically on first load. Click a link to open in a new tab (no collapse, opens immediately).
"""

import socket
import subprocess
import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# Ports and app paths (ROOT = folder containing main_ui.py)
ROOT = Path(__file__).resolve().parent

# Prefer project .venv Python so all sub-apps use same env
def _python_executable():
    venv_exe = ROOT / ".venv" / "Scripts" / "python.exe" if sys.platform == "win32" else ROOT / ".venv" / "bin" / "python"
    if venv_exe.exists():
        return str(venv_exe)
    return sys.executable

PORT_STORE_OPENING = 8502
PORT_MALL_DASHBOARD = 8503
PORT_MAP_DASHBOARD = 8504

APPS = [
    {
        "key": "store_opening",
        "icon": "🔍",
        "title": "Store Opening Discovery",
        "desc": "Search web for mall/store opening data, extract and analyze with AI. Get 2026 tenant and event info.",
        "port": PORT_STORE_OPENING,
        "cwd": ROOT / "googlesearch",
        "script": "app_streamlit.py",
        "button_text": "Click to Application"
    },
    {
        "key": "mall_dashboard",
        "icon": "🏬",
        "title": "Mall AI Dashboard",
        "desc": "Scrape mall directories, compare with old data, run Facebook/Instagram scrapers, and generate AI insights.",
        "port": PORT_MALL_DASHBOARD,
        "cwd": ROOT / "Mall_Ai_Dashboard",
        "script": "app.py",
        "button_text": "Click to Application"
    },
    {
        "key": "map_dashboard",
        "icon": "🗺️",
        "title": "Map Visual Analysis",
        "desc": "Analyze mall map screenshots with OCR and SBERT. Match with database and visualize missing tenants on the map.",
        "port": PORT_MAP_DASHBOARD,
        "cwd": ROOT / "Map scrapping",
        "script": "mall_analysis_app.py",
        "button_text": "Click to Application"
    },
]


def is_port_in_use(port: int) -> bool:
    """Return True if something is already listening on this port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def _find_free_port(start_port: int, max_tries: int = 20) -> int:
    """
    Find a free TCP port, starting at start_port and scanning upward.
    Returns the first available port, or start_port if none found within range.
    """
    port = start_port
    for _ in range(max_tries):
        if not is_port_in_use(port):
            return port
        port += 1
    # Fallback: return the original requested port (may still be in use)
    return start_port


def start_app(cwd: Path, script: str, preferred_port: int) -> int:
    """
    Start a Streamlit app in the background and return the actual port used.

    - We always try to start a *fresh* process so you don't accidentally
      reuse a stale server from an earlier run with old code.
    - If the preferred port is already in use, we scan upwards to find
      the next free port and use that.
    - stdout/stderr are inherited so each sub‑app's logs show in the same
      terminal where you run `streamlit run main_ui.py`.
    """
    app_path = cwd / script
    if not app_path.exists():
        # Could optionally show a Streamlit warning here, but simply return.
        return preferred_port

    actual_port = _find_free_port(preferred_port)

    subprocess.Popen(
        [
            _python_executable(),
            "-m",
            "streamlit",
            "run",
            str(app_path),
            "--server.port",
            str(actual_port),
            "--server.headless",
            "true",
        ],
        cwd=str(cwd),
        # Inherit stdout/stderr so logs appear in the main terminal
        stdout=None,
        stderr=None,
    )
    return actual_port


st.set_page_config(page_title="Combined Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# Start apps on first load (once per browser session) so links open immediately.
# We also remember the *actual* port each app was started on, since we may have
# to move to a different free port if the preferred one is already in use.
if "app_ports" not in st.session_state:
    st.session_state.app_ports = {}
    for app in APPS:
        actual_port = start_app(app["cwd"], app["script"], app["port"])
        st.session_state.app_ports[app["key"]] = actual_port

st.markdown("""
<style>
/* Base */
.stApp { background: linear-gradient(160deg, #0c1222 0%, #1a2332 40%, #0f172a 100%); color: #e2e8f0; min-height: 100vh; }
/* Header */
.dashboard-header { margin-bottom: 2.5rem; }
.dashboard-title { font-size: 2.25rem; font-weight: 800; color: #f8fafc; letter-spacing: -0.02em; margin: 0 0 0.35rem 0; }
.dashboard-subtitle { color: #64748b; font-size: 1rem; margin: 0; font-weight: 500; }

/* Cards: same height, flex layout */
/* Cards: vertical layout with full-width button */
.project-card {
    height: auto;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    background: linear-gradient(165deg, rgba(30,41,59,0.85) 0%, rgba(15,23,42,0.95) 100%);
    padding: 2.25rem;
    border-radius: 20px;
    border: 1px solid rgba(148,163,184,0.12);
    box-shadow: 0 4px 24px rgba(0,0,0,0.25), 0 0 0 1px rgba(255,255,255,0.03) inset;
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    margin-bottom: 2rem;
}
.project-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.35), 0 0 0 1px rgba(14,165,233,0.15);
    border-color: rgba(14,165,233,0.2);
}
.project-card-info {
    width: 100%;
}
.project-card-title { font-size: 1.6rem; font-weight: 800; color: #f1f5f9; margin: 0 0 0.75rem 0; line-height: 1.2; }
.project-card-desc {
    color: #94a3b8;
    font-size: 1.05rem;
    line-height: 1.6;
    margin: 0;
}
.project-card-cta-container {
    width: 100%;
    margin-top: 0.5rem;
}
.project-card-cta {
    display: flex;
    width: 100%;
    align-items: center;
    justify-content: center;
    padding: 1.5rem;
    background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
    color: white !important;
    border-radius: 14px;
    text-decoration: none;
    font-weight: 800;
    font-size: 1.4rem;
    transition: all 0.2s ease;
    box-shadow: 0 6px 20px rgba(14,165,233,0.4);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.project-card-cta:hover { 
    opacity: 0.95; 
    transform: scale(1.02); 
    box-shadow: 0 8px 30px rgba(14,165,233,0.5);
    color: white !important; 
}

/* Footer */
.dashboard-footer { margin-top: 2.5rem; padding-top: 1.25rem; border-top: 1px solid rgba(148,163,184,0.1); color: #64748b; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='dashboard-header'>
    <h1 class='dashboard-title'>Combined Dashboard</h1>
    <p class='dashboard-subtitle'>Access all your mall analysis tools from one place</p>
</div>
""", unsafe_allow_html=True)

# Vertical list of cards
for app in APPS:
    # Use the dynamically assigned port for each app (falls back to preferred)
    actual_port = st.session_state.app_ports.get(app["key"], app["port"])
    url = f"http://localhost:{actual_port}"
    st.markdown(
        f"""
        <div class='project-card'>
            <div class='project-card-info'>
                <div class='project-card-title'>{app['icon']} {app['title']}</div>
                <div class='project-card-desc'>{app['desc']}</div>
            </div>
            <div class='project-card-cta-container'>
                <a href='{url}' target='_blank' rel='noopener noreferrer' class='project-card-cta'>{app['button_text']}</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    '<p class="dashboard-footer">Apps start automatically when you open this page. If a tab shows "can\'t connect", wait a few seconds and click the link again.</p>',
    unsafe_allow_html=True,
)

