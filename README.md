# Combined Dashboard

One place to run all mall analysis tools: Store Opening Discovery, Mall AI Dashboard, and Map Visual Analysis. Use a single Python environment so every app has the same dependencies and runs without module errors.

---

## Prerequisites

- **Python 3.10+** (3.10 recommended)
- Windows (PowerShell) or macOS/Linux (bash)

---

## One-time setup

### 1. Clone or open the project

```powershell
cd C:\Users\Kavin\Desktop\Combined-dashboard-mall-comparison
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the environment

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

You should see `(.venv)` at the start of your prompt.

### 4. Install all dependencies

Install requirements for every app in one go:

```powershell
pip install -r "Map scrapping\requirements.txt" -r "Mall_Ai_Dashboard\requirements.txt" -r "googlesearch\requirements.txt"
```

---

## How to run

Always **activate the venv first**, then start the unified dashboard.

### Main Dashboard (Recommended)

One command starts the hub for all apps. This unified version works on a single port (8501) and is much more stable than the legacy multi-port version:

```powershell
.\.venv\Scripts\activate
streamlit run railway_app.py --server.port 8501
```

Then open **http://localhost:8501** in your browser.

---

## Ports and apps

The new unified dashboard runs everything on a **single port (8501)** using Streamlit's multi-page feature. This makes it compatible with Railway and simplifies local setup.

---

## Project structure

```
combined-dashboard/
├── railway_app.py          # Unified Entry Point (Local & Production)
├── main_ui.py              # Legacy wrapper (points to railway_app.py)
├── README.md               # This file
├── googlesearch/           # Store Opening Discovery
├── Mall_Ai_Dashboard/       # Mall AI Dashboard
└── Map scrapping/          # Map Visual Analysis
```

---

## Troubleshooting

- **"No module named 'easyocr'..."**  
  You're not using the project venv. Activate it (step 3) and run the `pip install` command (step 4).

- **Port already in use**  
  Stop any other Streamlit processes using port 8501.

---

## Quick reference

| Task | Command |
|------|---------|
| Create env | `python -m venv .venv` |
| Activate (Windows) | `.\.venv\Scripts\activate` |
| Install all deps | `pip install -r "Map scrapping\requirements.txt" -r "Mall_Ai_Dashboard\requirements.txt" -r "googlesearch\requirements.txt"` |
| Run dashboard | `streamlit run railway_app.py --server.port 8501` |
