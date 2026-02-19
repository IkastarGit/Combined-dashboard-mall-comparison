"""
Combined Dashboard - Railway Entry Point
"""

import json
import sys
from pathlib import Path
import streamlit as st

# Ports and app paths (ROOT = folder containing this script)
ROOT = Path(__file__).resolve().parent
SHARED_INPUT_FILE = ROOT / "shared_dashboard_input.json"

def load_shared_input() -> dict:
    """Load mall/search input from shared JSON. Returns dict with empty strings if missing."""
    default = {
        "mall_name": "",
        "address": "",
        "mall_homepage": "",
        "official_website": "",
        "mall_facebook_link": "",
        "mall_instagram_link": "",
        "hashtags_youtube_twitter": "",
        "googlesearch_query": "",
        "map_visual_url": "",
        "num_posts_to_scrape": 20,
    }
    if not SHARED_INPUT_FILE.exists():
        return default
    try:
        with open(SHARED_INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Handle num_posts_to_scrape separately to preserve integer type
        result = {**default, **{k: str(v).strip() if v is not None else "" for k, v in data.items() if k != "num_posts_to_scrape"}}
        if "num_posts_to_scrape" in data:
            try:
                result["num_posts_to_scrape"] = int(data["num_posts_to_scrape"])
            except (ValueError, TypeError):
                result["num_posts_to_scrape"] = default["num_posts_to_scrape"]
        return result
    except Exception:
        return default

def save_shared_input(data: dict) -> None:
    """Write mall/search input to shared JSON for sub-apps to read."""
    with open(SHARED_INPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

st.set_page_config(page_title="Combined Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Base: clean dark background */
.stApp {
    background: #0f1419;
    color: #e7e9ea;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Header */
.dashboard-header {
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.dashboard-title {
    font-size: 1.75rem;
    font-weight: 700;
    color: #fff;
    margin: 0 0 0.25rem 0;
}
.dashboard-subtitle {
    color: #8b98a5;
    font-size: 0.9375rem;
    margin: 0;
}

/* Cards: replicated from main_ui.py */
.project-card {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
    background: #192734;
    padding: 1.5rem 1.75rem;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 1rem;
    transition: border-color 0.15s ease, background 0.15s ease;
}
.project-card:hover {
    border-color: rgba(29,155,240,0.35);
    background: #1c2d3d;
}
.project-card-info { width: 100%; }
.project-card-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: #fff;
    margin: 0 0 0.5rem 0;
    line-height: 1.3;
}
.project-card-desc {
    color: #8b98a5;
    font-size: 0.875rem;
    line-height: 1.5;
    margin: 0;
}
.project-card-cta-container { width: 100%; margin-top: 0.25rem; }
.project-card-cta {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.4rem 0.9rem;
    background: #1d9bf0;
    color: #fff !important;
    border-radius: 9999px;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.8125rem;
    transition: background 0.15s ease, transform 0.15s ease, box-shadow 0.15s ease;
}
.project-card-cta:hover {
    background: #1a8cd8;
    color: #fff !important;
    transform: scale(1.04);
    box-shadow: 0 0 0 4px rgba(29,155,240,0.25);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='dashboard-header'>
    <h1 class='dashboard-title'>Webresearch Combined Dashboard</h1>
    <p class='dashboard-subtitle'>Select an application below or from the sidebar to begin.</p>
</div>
""", unsafe_allow_html=True)

# App Cards Section (Fixing localhost links to relative production-friendly links)
col1, col2, col3 = st.columns(3)

apps = [
    {
        "title": "Store Opening Discovery",
        "icon": "🔍",
        "desc": "Find mall and store opening data with AI. Extract 2026 tenant and event info from the web.",
        "link": "Store_Opening_Discovery" # Relative URL for Streamlit page
    },
    {
        "title": "Mall AI Dashboard",
        "icon": "🏬",
        "desc": "Scrape mall directories and Facebook/Instagram. Compare data over time and generate AI insights.",
        "link": "Mall_AI_Dashboard"
    },
    {
        "title": "Map Visual Analysis",
        "icon": "🗺️",
        "desc": "Analyze mall map screenshots with OCR. Match tenants to your database and see gaps on the map.",
        "link": "Map_Visual_Analysis"
    }
]

for i, app in enumerate(apps):
    with [col1, col2, col3][i]:
        st.markdown(f"""
        <div class='project-card'>
            <div class='project-card-info'>
                <div class='project-card-title'>{app['icon']} {app['title']}</div>
                <div class='project-card-desc'>{app['desc']}</div>
            </div>
            <div class='project-card-cta-container'>
                <a href='{app['link']}' target='_self' class='project-card-cta'>Open {app['title']}</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

with st.expander("📝 Mall & search inputs (optional — submit to pre-fill all three apps)", expanded=False):
    st.markdown("Enter data below and click **Submit** to save. The three apps use whatever was last submitted.")
    
    with st.form("shared_input_form"):
        mall_name = st.text_input("Mall Name", value="", placeholder="")
        address = st.text_input("Address *", value="", placeholder="Required", help="Required field")
        mall_homepage = st.text_input("Official Mall Website Homepage", value="", placeholder="https://...")
        official_website = st.text_input("Official Web Site Stores directory", value="", placeholder="https://...")
        mall_facebook_link = st.text_input("Mall Facebook Link", value="", placeholder="https://www.facebook.com/...")
        mall_instagram_link = st.text_input("Mall Instagram Link", value="", placeholder="https://www.instagram.com/...")
        num_posts_to_scrape = st.number_input("Number of Posts to Scrape", min_value=1, max_value=1000, value=20, step=1, help="Default: 20 posts. This value is used for both Facebook and Instagram scraping.")
        hashtags_youtube_twitter = st.text_input("Hashtags for use in Youtube, X(Twitter) Posts", value="", placeholder="#mall #shopping ...")
        googlesearch_query = st.text_area("Search query for Store Opening Discovery", value="", placeholder="e.g. Latest update about [mall name] · Coming soon tenants at [mall name]", height=80)
        map_visual_url = st.text_input("Mall Map URL (for Map Visual Analysis)", value="", placeholder="e.g. https://www.eg.comm/mall-name/map/#/")
        submitted = st.form_submit_button("Submit")
    if submitted:
        if not (address or "").strip():
            st.error("Address is required. Please enter the mall address.")
        else:
            save_shared_input({
                "mall_name": (mall_name or "").strip(),
                "address": (address or "").strip(),
                "mall_homepage": (mall_homepage or "").strip(),
                "official_website": (official_website or "").strip(),
                "mall_facebook_link": (mall_facebook_link or "").strip(),
                "mall_instagram_link": (mall_instagram_link or "").strip(),
                "hashtags_youtube_twitter": (hashtags_youtube_twitter or "").strip(),
                "googlesearch_query": (googlesearch_query or "").strip(),
                "map_visual_url": (map_visual_url or "").strip(),
                "num_posts_to_scrape": num_posts_to_scrape,
            })
            st.success("Saved. Open any of the apps above to begin.")

st.markdown("---")

# Merge Mall Tenants CSV with Excel Report (from Mall AI Dashboard + Map Scraping)
with st.expander("🔗 Merge Mall Tenants with Excel Report", expanded=False):
    st.markdown(
        "Upload the **Mall Tenants CSV** (from Mall AI Dashboard / map scraping) and the **Excel report** (mall research output). "
        "The merge will: replace **Proposed Floor Number** with the mall **floor**, fill **Proposed Shop Number** with **location_id**, "
        "and add **Latitude** and **Longitude** columns next to Proposed Shop Number, matching rows by tenant name."
    )
    col_merge_1, col_merge_2 = st.columns(2)
    with col_merge_1:
        merge_csv = st.file_uploader(
            "Mall Tenants CSV (e.g. mall_tenants_full.csv)",
            type=["csv"],
            key="merge_tenant_csv",
            help="CSV with columns: name, location_id, floor, latitude, longitude",
        )
    with col_merge_2:
        merge_excel = st.file_uploader(
            "Excel Report (e.g. mall_research_output.xlsx)",
            type=["xlsx"],
            key="merge_excel_report",
            help="Excel with sheet 'Existing Tennent Research'",
        )
    merge_btn = st.button("Merge and Download Excel", type="primary", key="merge_download_btn")
    if merge_btn and merge_csv and merge_excel:
        try:
            # We need to make sure merge_tenant_excel is in path
            if str(ROOT) not in sys.path:
                sys.path.append(str(ROOT))
                
            from merge_tenant_excel import merge_tenant_csv_with_excel
            csv_bytes = merge_csv.read()
            excel_bytes = merge_excel.read()
            out_bytes = merge_tenant_csv_with_excel(csv_bytes, excel_bytes)
            st.download_button(
                label="Download merged Excel",
                data=out_bytes,
                file_name="mall_research_output_merged.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_merged_excel",
            )
            st.success("Merge complete. Download ready.")
        except Exception as e:
            st.error(f"Merge failed: {e}")
            import traceback
            st.code(traceback.format_exc())
    elif merge_btn and (not merge_csv or not merge_excel):
        st.warning("Please upload both the Mall Tenants CSV and the Excel report.")

st.info("👈 You can also use the sidebar to navigate between applications.")
