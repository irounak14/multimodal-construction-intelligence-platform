import json
import os
from datetime import datetime
from typing import Any

import streamlit as st
from google import genai
from google.genai import types

# -------------------------------------------------------------------
# BuildSense | Multimodal Construction Intelligence Platform
# Streamlit Community Cloud-ready; no external database required.
# -------------------------------------------------------------------

st.set_page_config(
    page_title="BuildSense | Construction Intelligence",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- Theme --------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root { --ink:#142033; --muted:#68758a; --line:#e6ebf2; --blue:#315efb; --blue2:#2447ce; --soft:#f4f7fc; --green:#087f5b; --amber:#a85d00; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background: #f7f9fc; color:var(--ink); }
header[data-testid="stHeader"] { background:rgba(247,249,252,.9); }
.block-container { max-width: 1380px; padding-top: 1.8rem; padding-bottom: 3rem; }
section[data-testid="stSidebar"] { background:#101827; border-right:1px solid #202c3f; }
section[data-testid="stSidebar"] * { color:#e9eef7 !important; }
section[data-testid="stSidebar"] .stRadio label { background:#172338; padding:10px 12px; border-radius:10px; margin-bottom:5px; border:1px solid #26354c; }
section[data-testid="stSidebar"] .stRadio label:hover { background:#22324c; }
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color:#aebbd0 !important; }
.brand { display:flex; align-items:center; gap:12px; padding:8px 2px 22px; }
.brand-icon { width:44px; height:44px; display:flex; align-items:center; justify-content:center; background:linear-gradient(135deg,#ffcc65,#ff8a36); border-radius:13px; font-size:24px; box-shadow:0 8px 24px #ff9e3830; }
.brand-name { font-family:'Manrope',sans-serif; font-weight:800; font-size:23px; letter-spacing:-.7px; color:white; }
.brand-sub { font-size:11px; color:#aab8cd; margin-top:2px; }
.eyebrow { color:var(--blue); text-transform:uppercase; letter-spacing:1.7px; font-weight:800; font-size:11px; margin-bottom:8px; }
.hero-title { font-family:'Manrope',sans-serif; font-size:38px; line-height:1.12; font-weight:800; letter-spacing:-1.3px; color:#142033; margin:0; }
.hero-copy { color:#68758a; font-size:15px; line-height:1.7; max-width:800px; margin-top:12px; }
.hero { background:linear-gradient(120deg,#ffffff 0%,#eef3ff 100%); border:1px solid #e3eaf8; border-radius:22px; padding:30px 32px; margin-bottom:22px; box-shadow:0 10px 35px #1d35570a; }
.pill { display:inline-block; background:#e7edff; color:#2447ce; border:1px solid #d7e0ff; padding:5px 10px; border-radius:99px; font-size:11px; font-weight:800; margin-bottom:14px; }
.metric { background:white; border:1px solid var(--line); border-radius:16px; padding:18px 20px; box-shadow:0 5px 18px #14203305; min-height:112px; }
.metric-label { font-size:12px; color:#718096; font-weight:600; }
.metric-value { font-family:'Manrope',sans-serif; font-size:29px; color:#142033; font-weight:800; margin-top:8px; }
.metric-note { font-size:11px; color:#8b96a8; margin-top:3px; }
.section-title { font-family:'Manrope',sans-serif; font-size:22px; font-weight:800; letter-spacing:-.5px; margin:18px 0 5px; }
.section-copy { color:#718096; font-size:13px; margin-bottom:15px; }
.card { background:white; border:1px solid var(--line); border-radius:16px; padding:20px; height:100%; }
.card-icon { font-size:23px; margin-bottom:12px; }
.card-title { font-family:'Manrope',sans-serif; font-size:16px; font-weight:800; margin-bottom:6px; color:#172238; }
.card-copy { font-size:13px; line-height:1.65; color:#6b778c; }
.card-tag { display:inline-block; background:#f1f4f9; color:#5b6880; border-radius:7px; padding:4px 8px; font-size:10px; font-weight:800; margin-top:13px; }
.notice { background:#fff8e8; border:1px solid #f6e3b5; color:#79530b; padding:13px 16px; border-radius:12px; font-size:12px; line-height:1.6; }
.success-box { background:#eaf8f1; border:1px solid #c9efdc; color:#126843; padding:13px 16px; border-radius:12px; font-size:13px; }
div.stButton > button[kind="primary"] { background:var(--blue); border:0; border-radius:10px; padding:.65rem 1rem; font-weight:700; }
div.stButton > button[kind="primary"]:hover { background:var(--blue2); }
.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea { border-radius:10px; }
hr { border-color:#e7ebf2; }
footer {visibility:hidden;}
.small-muted { color:#7d899b; font-size:11px; }
</style>
""", unsafe_allow_html=True)

# -------------------------- Secrets / AI -----------------------------
def get_api_key() -> str:
    key = ""
    try:
        key = str(st.secrets.get("GEMINI_API_KEY", "")).strip()
    except Exception:
        pass
    if not key:
        key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        key = st.session_state.get("gemini_api_key", "").strip()
    return key

def call_gemini(prompt: str, image_bytes: bytes | None = None, mime_type: str = "image/jpeg") -> dict[str, Any]:
    key = get_api_key()
    if not key:
        raise RuntimeError("No Gemini API key configured. Add it in the sidebar or Streamlit app Secrets.")
    client = genai.Client(api_key=key)
    contents: list[Any] = [prompt + "\nReturn ONLY valid JSON. Do not wrap it in markdown."]
    if image_bytes:
        contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))
    model = "gemini-2.5-flash"
    response = client.models.generate_content(model=model, contents=contents)
    raw = (response.text or "").strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    parsed = json.loads(raw)
    if not isinstance(parsed, dict):
        raise ValueError("The AI response was not a JSON object.")
    return parsed

def safe_demo(kind: str) -> dict[str, Any]:
    if kind == "safety":
        return {
            "safety_score": 76, "overall_status": "Needs attention",
            "ppe_checklist": [
                {"item":"Safety helmet","status":"Visible / verify fit","notes":"Check that the helmet is properly secured."},
                {"item":"High-visibility vest","status":"Not clearly verifiable","notes":"Ensure every worker in active zones wears a high-visibility vest."},
                {"item":"Safety footwear","status":"Not verifiable from image","notes":"Confirm compliant protective footwear on site."},
                {"item":"Safety harness","status":"Conditional","notes":"Use fall protection where required for work at height."}
            ],
            "hazards":[
                {"hazard":"Unprotected edge or elevated work area","severity":"High","remedy":"Install compliant edge protection and verify fall-protection controls."},
                {"hazard":"Housekeeping / trip risk","severity":"Medium","remedy":"Keep walkways clear and materials properly stacked."}
            ],
            "summary":"Demonstration result only. Inspect the site in person and verify PPE with the site safety officer."
        }
    if kind == "crack":
        return {
            "defect_type":"Possible surface crack (demo)",
            "estimated_width_mm":"Not measurable from this image alone",
            "urgency":"Requires professional inspection",
            "possible_causes":["Drying shrinkage","Thermal movement","Settlement (cannot be ruled out from a photo)"],
            "recommended_actions":["Record crack location and date","Measure width with a crack gauge","Check for change over time","Ask a qualified structural engineer to inspect if widening, diagonal, or associated with movement"],
            "summary":"Demonstration result only. A photo cannot establish structural safety or a reliable crack width."
        }
    return {}

def json_download(data: dict[str, Any], filename: str):
    st.download_button("⬇ Download JSON report", json.dumps(data, indent=2), file_name=filename, mime="application/json")

def page_header(kicker: str, title: str, copy: str):
    st.markdown(f'<div class="eyebrow">{kicker}</div><h1 class="hero-title">{title}</h1><p class="hero-copy">{copy}</p>', unsafe_allow_html=True)

def metric(label: str, value: str, note: str = ""):
    st.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>', unsafe_allow_html=True)

# ----------------------------- Sidebar -------------------------------
with st.sidebar:
    st.markdown("""
    <div class="brand">
      <div class="brand-icon">🏗️</div>
      <div><div class="brand-name">BuildSense</div><div class="brand-sub">CONSTRUCTION INTELLIGENCE</div></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px;font-weight:800;letter-spacing:1.6px;color:#8493aa;margin:2px 0 10px;">WORKSPACE</div>', unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        ["Overview", "Site Safety & PPE", "Crack Diagnostics", "Real Estate Valuation", "Daily Site Assistant", "Architecture & Stack"],
        label_visibility="collapsed",
        format_func=lambda x: {
            "Overview":"⌂  Overview",
            "Site Safety & PPE":"⛑️  Site Safety & PPE",
            "Crack Diagnostics":"⌁  Crack Diagnostics",
            "Real Estate Valuation":"▦  Real Estate Valuation",
            "Daily Site Assistant":"☀️  Daily Site Assistant",
            "Architecture & Stack":"⌘  Architecture & Stack",
        }[x],
    )
    st.markdown("---")
    st.markdown('<div style="font-size:10px;font-weight:800;letter-spacing:1.6px;color:#8493aa;margin-bottom:8px;">AI CONFIGURATION</div>', unsafe_allow_html=True)
    st.caption("Your key is used for this session and is not displayed.")
    sidebar_key = st.text_input("Gemini API key", type="password", placeholder="Paste API key", help="Alternatively add GEMINI_API_KEY in Streamlit app Settings → Secrets.")
    if sidebar_key:
        st.session_state["gemini_api_key"] = sidebar_key.strip()
    if get_api_key():
        st.markdown('<div style="font-size:12px;color:#86efac;">● Gemini configured</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:12px;color:#fcd34d;">● Demo mode (no API key)</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div style="font-size:11px;color:#9eacc0;line-height:1.6;">Built for construction teams<br>Multimodal AI · Structured reports · INR</div>', unsafe_allow_html=True)

# ----------------------------- Overview ------------------------------
if page == "Overview":
    st.markdown("""
    <div class="hero">
      <span class="pill">SKILL WALLET · CAPSTONE PROJECT 01</span>
      <div class="hero-title">Smarter construction.<br><span style="color:#315efb;">Safer decisions.</span></div>
      <div class="hero-copy">A multimodal AI workspace for construction-site safety, crack diagnostics, property estimates, and weather-aware daily guidance — bringing visual inputs and structured insights into one place.</div>
    </div>
    """, unsafe_allow_html=True)
    a,b,c,d = st.columns(4)
    with a: metric("INTELLIGENCE MODULES","04","Visual + planning workflows")
    with b: metric("REPORT FORMAT","JSON","Downloadable structured output")
    with c: metric("CURRENCY","INR","Indian property estimates")
    with d: metric("AI ENGINE","Gemini","Demo fallback available")
    st.markdown('<div class="section-title">Explore the platform</div><div class="section-copy">Choose a module from the sidebar or open a workspace below.</div>', unsafe_allow_html=True)
    cols = st.columns(2)
    cards = [
        ("⛑️","Site Safety & PPE","Review a site photo for visible PPE compliance, potential hazards, severity, and corrective actions.","IMAGE ANALYSIS","Site Safety & PPE"),
        ("🧱","Crack Diagnostics","Classify visible surface defects, explore possible causes, and plan the next inspection steps.","IMAGE ANALYSIS","Crack Diagnostics"),
        ("🏙️","Real Estate Valuation","Estimate an indicative project value and cost breakdown from building and location inputs.","COST ESTIMATION","Real Estate Valuation"),
        ("🌦️","Daily Site Assistant","Create weather-aware precautions and ask a multi-turn construction guidance assistant.","SITE GUIDANCE","Daily Site Assistant"),
    ]
    for i, item in enumerate(cards):
        col = cols[i % 2]
        icon,title,copy,tag,dest = item
        with col:
            st.markdown(f'<div class="card"><div class="card-icon">{icon}</div><div class="card-title">{title}</div><div class="card-copy">{copy}</div><div class="card-tag">{tag}</div></div>', unsafe_allow_html=True)
            if st.button(f"Open {title} →", key=f"open_{i}", use_container_width=True):
                st.session_state["requested_page"] = dest
                st.rerun()
    if st.session_state.get("requested_page"):
        # Sidebar radio is the source of truth on reruns; explain quick navigation.
        st.info(f"Use the left navigation to open **{st.session_state.pop('requested_page')}**.")
    st.markdown("---")
    st.markdown('<div class="notice">⚠️ <b>Important:</b> Outputs are preliminary decision support, not a safety certification, structural diagnosis, engineering design, legal valuation, or substitute for qualified professionals. Verify all findings on site.</div>', unsafe_allow_html=True)

# ----------------------------- Safety --------------------------------
elif page == "Site Safety & PPE":
    page_header("EPIC 02 · VISUAL INSPECTION", "Site Safety & PPE Review", "Upload a construction-site photo to review visible personal protective equipment and potential hazards.")
    left,right = st.columns([1,1.2], gap="large")
    with left:
        upload = st.file_uploader("Upload construction site photo", type=["jpg","jpeg","png"], key="safety_upload")
        if upload:
            st.image(upload, caption="Uploaded site image", use_container_width=True)
        st.markdown('<div class="notice">AI cannot reliably verify hidden PPE, certification labels, fit, or compliance from a single photo. Treat results as a prompt for human inspection.</div>', unsafe_allow_html=True)
        run = st.button("Analyze site safety", type="primary", use_container_width=True)
    with right:
        if run:
            with st.spinner("Reviewing visible safety indicators..."):
                try:
                    if upload:
                        prompt = """You are a construction safety assistant. Inspect the attached construction-site photo. Return JSON with keys: safety_score (integer 0-100, only a preliminary visual impression), overall_status (short string), ppe_checklist (array of objects with item, status, notes), hazards (array of objects with hazard, severity [Low/Medium/High/Critical], remedy), summary (string). Assess visible helmets, high-visibility vests, safety footwear only if visible, and harnesses only where relevant. Do not claim certainty when not visible. Do not assert compliance with OSHA/IS 456 from a photo. Flag visible hazards conservatively."""
                        data = call_gemini(prompt, upload.getvalue(), upload.type or "image/jpeg")
                        source = "Gemini visual analysis"
                    else:
                        data = safe_demo("safety")
                        source = "Demo sample"
                    st.session_state["safety_result"] = data
                    st.session_state["safety_source"] = source
                except Exception as e:
                    st.error(f"AI analysis could not run: {e}")
        data = st.session_state.get("safety_result")
        if data:
            score = data.get("safety_score", "—")
            status = data.get("overall_status", "Review")
            x,y = st.columns(2)
            with x: metric("PRELIMINARY SAFETY SCORE", f"{score}/100", "Visual screening only")
            with y: metric("OVERALL STATUS", str(status), st.session_state.get("safety_source",""))
            st.markdown('<div class="section-title">PPE checklist</div>', unsafe_allow_html=True)
            for item in data.get("ppe_checklist", []):
                if isinstance(item, dict):
                    with st.container(border=True):
                        st.markdown(f"**{item.get('item','PPE item')}** · {item.get('status','Not specified')}")
                        st.caption(item.get("notes",""))
            st.markdown('<div class="section-title">Potential hazards & remedies</div>', unsafe_allow_html=True)
            for h in data.get("hazards", []):
                if isinstance(h, dict):
                    sev = h.get("severity","Unrated")
                    st.markdown(f"**{sev}** — {h.get('hazard','Hazard not specified')}")
                    st.write(h.get("remedy",""))
            st.info(data.get("summary","Preliminary guidance only."))
            json_download(data, "buildsense_site_safety_report.json")
        else:
            st.markdown('<div class="card"><div class="card-icon">🔎</div><div class="card-title">Your safety report will appear here</div><div class="card-copy">Upload a photo and run the review to generate a score, PPE checklist, hazard list, and recommended actions.</div></div>', unsafe_allow_html=True)

# ----------------------------- Crack ---------------------------------
elif page == "Crack Diagnostics":
    page_header("EPIC 02 · STRUCTURAL SCREENING", "Crack Diagnostics", "Review a photo of a concrete or wall surface and get a cautious, structured first-pass assessment.")
    left,right = st.columns([1,1.2], gap="large")
    with left:
        upload = st.file_uploader("Upload crack / wall photo", type=["jpg","jpeg","png"], key="crack_upload")
        if upload: st.image(upload, caption="Uploaded surface image", use_container_width=True)
        st.markdown('<div class="notice">A photo cannot establish structural integrity or reliably measure crack width without scale and site context. Seek an engineer for significant or changing cracks.</div>', unsafe_allow_html=True)
        run = st.button("Review crack image", type="primary", use_container_width=True)
    with right:
        if run:
            with st.spinner("Reviewing the visible surface..."):
                try:
                    if upload:
                        prompt = """You are an assistant for preliminary construction defect triage. Inspect the attached surface photo. Return JSON with keys: defect_type, estimated_width_mm, urgency, possible_causes (array of strings), recommended_actions (array of strings), summary. Defect categories may include hairline, settlement-like, shear-like, thermal movement, spalling, or uncertain. Never claim a definitive structural diagnosis or precise crack width from pixels alone; use 'not measurable from image alone' where appropriate. Recommend qualified inspection for concerning signs."""
                        data = call_gemini(prompt, upload.getvalue(), upload.type or "image/jpeg")
                        source = "Gemini visual analysis"
                    else:
                        data = safe_demo("crack")
                        source = "Demo sample"
                    data["analysis_source"] = source
                    st.session_state["crack_result"] = data
                except Exception as e:
                    st.error(f"AI review could not run: {e}")
        data = st.session_state.get("crack_result")
        if data:
            x,y = st.columns(2)
            with x: metric("POSSIBLE DEFECT", str(data.get("defect_type","Uncertain")), "Preliminary classification")
            with y: metric("URGENCY", str(data.get("urgency","Review")), data.get("analysis_source",""))
            st.markdown('<div class="section-title">Estimated width</div>', unsafe_allow_html=True)
            st.write(data.get("estimated_width_mm","Not measurable from image alone"))
            st.markdown('<div class="section-title">Possible causes</div>', unsafe_allow_html=True)
            for cause in data.get("possible_causes", []): st.markdown(f"- {cause}")
            st.markdown('<div class="section-title">Recommended next steps</div>', unsafe_allow_html=True)
            for action in data.get("recommended_actions", []): st.markdown(f"- {action}")
            st.info(data.get("summary","Preliminary guidance only."))
            json_download(data, "buildsense_crack_review.json")
        else:
            st.markdown('<div class="card"><div class="card-icon">🧱</div><div class="card-title">Your crack review will appear here</div><div class="card-copy">Generate a preliminary defect category, potential causes, urgency, and follow-up inspection actions.</div></div>', unsafe_allow_html=True)

# ----------------------------- Valuation -----------------------------
elif page == "Real Estate Valuation":
    page_header("EPIC 03 · PLANNING & ESTIMATION", "Real Estate Valuation", "Create an indicative early-stage cost and asset estimate using project size, location tier, structure type, and completion progress.")
    col1,col2,col3 = st.columns(3)
    with col1:
        structure = st.selectbox("Structure type", ["Residential","Commercial","Industrial","Institutional"])
        area = st.number_input("Built-up area (sq ft)", min_value=100, max_value=2000000, value=1500, step=100)
    with col2:
        tier = st.selectbox("Location tier", ["Tier 1 city","Tier 2 city","Tier 3 city"])
        completion = st.slider("Completion percentage", 0, 100, 25, 5)
    with col3:
        quality = st.selectbox("Construction finish", ["Economical","Standard","Premium"])
        market_factor = st.number_input("Local market factor (optional)", min_value=0.5, max_value=3.0, value=1.0, step=0.1)
    rates = {
        "Residential":{"Economical":1700,"Standard":2200,"Premium":3000},
        "Commercial":{"Economical":2000,"Standard":2800,"Premium":3900},
        "Industrial":{"Economical":1400,"Standard":1900,"Premium":2600},
        "Institutional":{"Economical":1900,"Standard":2600,"Premium":3600},
    }
    tier_factor = {"Tier 1 city":1.25,"Tier 2 city":1.0,"Tier 3 city":0.82}[tier]
    rate = rates[structure][quality] * tier_factor
    estimated_budget = area * rate
    incurred = estimated_budget * completion / 100
    asset_value = estimated_budget * market_factor * (0.75 + 0.25 * completion / 100)
    steel_kg = area * (3.5 if structure == "Industrial" else 4.0 if structure == "Residential" else 4.5)
    cement_bags = area * (0.35 if structure == "Industrial" else 0.40 if structure == "Residential" else 0.45)
    st.markdown('<div class="section-title">Indicative project estimate</div><div class="section-copy">Illustrative planning numbers only. Replace default rates with local BOQ, contractor quotes, and current market data.</div>', unsafe_allow_html=True)
    m1,m2,m3,m4 = st.columns(4)
    with m1: metric("PROJECT BUDGET", f"₹{estimated_budget/100000:.2f} L", f"₹{rate:,.0f} / sq ft")
    with m2: metric("CAPEX INCURRED", f"₹{incurred/100000:.2f} L", f"{completion}% progress input")
    with m3: metric("INDICATIVE ASSET VALUE", f"₹{asset_value/100000:.2f} L", f"Market factor {market_factor:.1f}×")
    with m4: metric("MATERIAL PLANNING", f"{steel_kg/1000:.2f} t", f"~{cement_bags:,.0f} cement bags")
    st.progress(completion / 100, text=f"Milestone progress: {completion}%")
    st.markdown('<div class="section-title">Budget breakdown</div>', unsafe_allow_html=True)
    breakdown = {"Structure & foundation":0.32,"Finishes":0.22,"MEP services":0.18,"Labour":0.18,"Contingency & other":0.10}
    for name, share in breakdown.items():
        amount = estimated_budget * share
        st.markdown(f"**{name}** · ₹{amount/100000:.2f} L ({share:.0%})")
        st.progress(share)
    report = {
        "generated_at":datetime.now().isoformat(timespec="seconds"),"structure_type":structure,
        "built_up_area_sqft":area,"location_tier":tier,"completion_percent":completion,
        "finish_quality":quality,"local_market_factor":market_factor,
        "estimated_cost_per_sqft_inr":round(rate,2),"estimated_project_budget_inr":round(estimated_budget,2),
        "estimated_capex_incurred_inr":round(incurred,2),"indicative_asset_value_inr":round(asset_value,2),
        "indicative_steel_kg":round(steel_kg,2),"indicative_cement_bags":round(cement_bags,0),
        "budget_breakdown_percent":{k:round(v*100) for k,v in breakdown.items()},
        "disclaimer":"Illustrative estimate only; not a formal valuation, BOQ, or engineering quantity survey."
    }
    json_download(report,"buildsense_valuation_report.json")
    st.markdown('<div class="notice">Material quantities are broad thumb-rule estimates, not construction specifications. Have a qualified engineer or quantity surveyor verify them before procurement.</div>', unsafe_allow_html=True)

# ----------------------------- Daily assistant -----------------------
elif page == "Daily Site Assistant":
    page_header("EPIC 05 · DAILY SITE GUIDANCE", "Daily Site Assistant", "Select current site conditions for practical precautions, then ask follow-up questions in a construction-focused assistant.")
    weather = st.selectbox("Current / expected site condition", ["Normal","High wind","Heavy rain","Extreme heat"])
    site_task = st.selectbox("Main activity today", ["General construction","Crane / lifting operations","Electrical work","Concrete pouring / curing","Work at height","Excavation"])
    precautions = {
        "Normal":["Hold the toolbox talk and confirm today's work permits.","Keep access paths clear and inspect PPE before work begins.","Check equipment, barricades, and emergency access."],
        "High wind":["Pause crane and lifting operations when wind exceeds the equipment/site limit.","Secure loose materials, sheets, and temporary structures.","Avoid work at height when wind makes the task unsafe; follow the site wind action plan."],
        "Heavy rain":["Review drainage, slippery surfaces, and excavation stability.","Protect electrical equipment and keep connections away from standing water.","Delay lifting, roof work, or excavation where conditions are unsafe; follow site procedures."],
        "Extreme heat":["Provide drinking water, shaded rest, and acclimatization breaks.","Schedule strenuous work for cooler periods where possible.","Watch for heat illness symptoms and follow the site's emergency response plan."]
    }
    st.markdown('<div class="section-title">Site condition advisory</div>', unsafe_allow_html=True)
    for p in precautions[weather]: st.markdown(f"- {p}")
    task_extra = {
        "Crane / lifting operations":"Confirm lift plan, exclusion zone, competent operator, rigging inspection, and weather limits.",
        "Electrical work":"Use authorized personnel, isolation/lockout procedures, and inspected tools; never work on live equipment unless an approved procedure explicitly permits it.",
        "Concrete pouring / curing":"Follow the approved mix and curing method; protect fresh concrete from extreme weather and avoid adding water without engineering approval.",
        "Work at height":"Verify access equipment, guardrails, anchor points, fall protection, and rescue arrangements.",
        "Excavation":"Check utility locations, protective systems, access/egress, water accumulation, and competent-person inspections.",
        "General construction":"Coordinate trades, confirm permits, maintain housekeeping, and keep first-aid/emergency routes accessible."
    }
    st.info(task_extra[site_task])
    if "assistant_messages" not in st.session_state:
        st.session_state["assistant_messages"] = [{"role":"assistant","content":"Hi! I can help with general construction planning and site precautions. Tell me about the activity, conditions, or issue you are working through."}]
    st.markdown('<div class="section-title">Construction assistant</div>', unsafe_allow_html=True)
    for msg in st.session_state["assistant_messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    question = st.chat_input("Ask about a construction task, materials, planning...")
    if question:
        st.session_state["assistant_messages"].append({"role":"user","content":question})
        with st.chat_message("user"): st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Preparing guidance..."):
                try:
                    history = st.session_state["assistant_messages"][-8:]
                    prompt = f"""You are BuildSense, a construction-site planning assistant. Current weather: {weather}. Main activity: {site_task}. Give concise, practical general guidance, ask clarifying questions if needed, and prioritize worker safety. Never replace a qualified engineer, site safety officer, local codes, or approved method statements. Conversation so far:\n{json.dumps(history)}\nReply to the latest user message in plain text."""
                    if get_api_key():
                        client = genai.Client(api_key=get_api_key())
                        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                        answer = (response.text or "").strip() or "I couldn't generate a response. Please try again."
                    else:
                        answer = f"Demo guidance for **{site_task.lower()}** in **{weather.lower()}** conditions: {task_extra[site_task]} For a specific recommendation, confirm site procedures and consult the responsible supervisor or engineer."
                    st.markdown(answer)
                except Exception as e:
                    answer = f"I couldn't reach the AI service: {e}"
                    st.error(answer)
        st.session_state["assistant_messages"].append({"role":"assistant","content":answer})

# ----------------------------- Architecture --------------------------
elif page == "Architecture & Stack":
    page_header("PLATFORM OVERVIEW", "Architecture & Technology Stack", "A simple, deployable architecture designed for a capstone demo and straightforward iteration.")
    st.markdown('<div class="section-title">How the app works</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown('<div class="card"><div class="card-icon">🖥️</div><div class="card-title">1. Streamlit UI</div><div class="card-copy">Inputs, image upload, project estimates, weather selector, chat interface, and downloadable reports.</div><div class="card-tag">PRESENTATION LAYER</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><div class="card-icon">🧠</div><div class="card-title">2. Gemini Multimodal LLM</div><div class="card-copy">Interprets uploaded site imagery and produces structured JSON responses. Without a key, selected workflows use demo mode.</div><div class="card-tag">AI / REASONING</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card"><div class="card-icon">📦</div><div class="card-title">3. JSON contracts</div><div class="card-copy">Results are displayed in the UI and can be downloaded as JSON. This Streamlit version does not require an external database.</div><div class="card-tag">OUTPUT LAYER</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Technology stack</div>', unsafe_allow_html=True)
    stack = [
        ("Python 3.9+","Application logic and calculations"),
        ("Streamlit","Interactive UI and Community Cloud deployment"),
        ("Google Gemini API","Multimodal image review and conversational guidance"),
        ("Pillow / image bytes","Image input handling through Streamlit upload"),
        ("JSON","Consistent, downloadable report format"),
        ("GitHub","Version control and deployment source"),
    ]
    for name,desc in stack:
        st.markdown(f"**{name}** — {desc}")
    st.markdown("---")
    st.markdown('<div class="notice">Safety, structural and valuation outputs are preliminary. Always validate decisions with qualified professionals, approved drawings, local requirements, and current site data.</div>', unsafe_allow_html=True)
