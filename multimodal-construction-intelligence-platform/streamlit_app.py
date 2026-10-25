import streamlit as st
from backend.app.ai import generate_json
from backend.app.database import init_db, save_analysis, list_analyses
from backend.app.schemas import ValuationRequest, PlanRequest, DailyRequest

st.set_page_config(page_title="BuildSense", page_icon="🏗️", layout="wide")
init_db()
st.title("🏗️ BuildSense")
st.caption("Multimodal Construction Intelligence Platform")
st.warning("Preliminary guidance only. This app does not certify safety or replace qualified professionals.")

def report(kind, title, result):
    saved = save_analysis(kind, title, result.get("headline", title), result)
    st.success(f"Saved report #{saved['id']}")
    st.subheader(result.get("headline", title))
    st.json(result)

page = st.sidebar.radio("Navigation", [
    "Dashboard", "Site Safety", "Crack Review", "Property Valuation",
    "Construction Planning", "Daily Assistance", "Analysis History"
])

if page == "Dashboard":
    items = list_analyses(100)
    a, b, c, d = st.columns(4)
    a.metric("Total analyses", len(items))
    b.metric("Safety reviews", sum(x["kind"] == "site_safety" for x in items))
    c.metric("Crack reviews", sum(x["kind"] == "crack" for x in items))
    d.metric("Planning reports", sum(x["kind"] == "plan" for x in items))
    st.subheader("Recent reports")
    for item in items[:5]:
        with st.expander(item["title"]):
            st.write(item["summary"])
            st.json(item["result"])

elif page in ("Site Safety", "Crack Review"):
    safety = page == "Site Safety"
    image = st.file_uploader("Upload construction photo", type=["jpg", "jpeg", "png", "webp"])
    context = st.text_area("Site context / observations")
    if image:
        st.image(image, width=500)
    if st.button("Analyze", type="primary"):
        if not image:
            st.error("Please upload an image first.")
        else:
            if safety:
                kind, title = "site_safety", "Site safety review"
                fallback = {"headline":"Preliminary site safety review","risk_level":"Review required",
                    "observations":["Confirm task-appropriate PPE.","Check access, edge protection and housekeeping.","Secure equipment and materials."],
                    "recommended_actions":["Ask a site supervisor to inspect in person.","Log hazards and corrective actions."],
                    "limitations":"Demo mode does not interpret image pixels."}
                prompt = f"Review this construction photo for possible safety concerns. Context: {context}. Return JSON keys headline, risk_level, observations array, recommended_actions array, limitations. Do not certify compliance."
            else:
                kind, title = "crack", "Crack observation"
                fallback = {"headline":"Preliminary crack observation","severity":"Unknown — professional inspection required",
                    "observations":["A photo cannot determine crack depth or structural significance.","Record location, length, width and date.","Monitor changes or water ingress."],
                    "recommended_actions":["Arrange a qualified structural inspection for concerning or widening cracks."],
                    "limitations":"Not a structural diagnosis."}
                prompt = f"Review this construction photo for possible cracks. Context: {context}. Return JSON keys headline, severity, observations array, recommended_actions array, limitations. Never diagnose structural safety from a photo."
            with st.spinner("Analyzing..."):
                result, mode = generate_json(prompt, fallback, image.getvalue(), image.type)
            result["mode"] = mode
            result["context"] = context
            report(kind, title, result)

elif page == "Property Valuation":
    st.subheader("Indicative Property Valuation")
    with st.form("valuation"):
        location = st.text_input("Location")
        property_type = st.selectbox("Property type", ["Residential", "Commercial", "Industrial", "Land"])
        area = st.number_input("Area (sq ft)", min_value=1.0, value=1000.0)
        rate = st.number_input("Estimated rate per sq ft (₹)", min_value=1.0, value=3000.0)
        age = st.number_input("Age in years", min_value=0, max_value=300, value=5)
        condition = st.selectbox("Condition", ["Excellent", "Good", "Fair", "Needs repair"], index=1)
        submit = st.form_submit_button("Calculate")
    if submit:
        try:
            req = ValuationRequest(location=location, property_type=property_type, area_sqft=area,
                rate_per_sqft=rate, age_years=int(age), condition=condition)
            base = req.area_sqft * req.rate_per_sqft
            age_factor = max(.55, 1 - req.age_years * .008)
            cond = {"Excellent":1.08, "Good":1.0, "Fair":.9, "Needs repair":.75}.get(req.condition, 1.0)
            estimate = round(base * age_factor * cond)
            fallback = {"headline":"Indicative property value estimate","estimated_value_inr":estimate,
                "range_inr":{"low":round(estimate*.9),"high":round(estimate*1.1)},
                "calculation":f"{req.area_sqft:,.0f} sq ft × ₹{req.rate_per_sqft:,.0f}/sq ft, adjusted for age and condition.",
                "factors_to_verify":["Recent comparable sales","Exact location","Title and approvals","Construction quality"],
                "limitations":"Rule-of-thumb estimate, not a formal appraisal."}
            result, mode = generate_json(f"Comment on estimate inputs {req.model_dump()}, arithmetic estimate INR {estimate}. Return JSON keys headline, estimated_value_inr, range_inr low/high, calculation, factors_to_verify array, limitations. Do not invent live market data.", fallback)
            result.update(mode=mode, inputs=req.model_dump())
            report("valuation", f"Valuation — {location}", result)
        except Exception as e:
            st.error(f"Please check the inputs: {e}")

elif page == "Construction Planning":
    with st.form("plan"):
        name = st.text_input("Project name")
        project_type = st.selectbox("Project type", ["Residential", "Commercial", "Industrial"])
        area = st.number_input("Site area (sq ft)", min_value=1.0, value=2000.0)
        floors = st.number_input("Floors", min_value=1, max_value=150, value=2)
        months = st.number_input("Target months", min_value=1, max_value=240, value=12)
        budget = st.number_input("Budget (₹)", min_value=1.0, value=5000000.0)
        notes = st.text_area("Additional notes")
        submit = st.form_submit_button("Generate Plan")
    if submit:
        try:
            req = PlanRequest(project_name=name, project_type=project_type, site_area_sqft=area,
                floors=int(floors), target_months=int(months), budget_inr=budget, notes=notes)
            fallback = {"headline":f"Draft delivery plan: {name}",
                "phases":[{"phase":"Requirements and approvals","duration":"10%","tasks":["Confirm scope and approvals."]},
                {"phase":"Design and procurement","duration":"15%","tasks":["Coordinate drawings and materials."]},
                {"phase":"Foundation","duration":"20%","tasks":["Complete approved groundwork."]},
                {"phase":"Structure","duration":"30%","tasks":["Sequence structural work with inspections."]},
                {"phase":"Services and finishes","duration":"20%","tasks":["Install and test services."]},
                {"phase":"Handover","duration":"5%","tasks":["Complete quality checks."]}],
                "milestones":["Approvals","Foundation sign-off","Structure complete","Services tested","Handover"],
                "risks":["Weather delays","Material delays","Design gaps","Rework"],
                "next_steps":["Validate timeline with professionals.","Assign owners and contingency."],
                "limitations":"Planning template; professional validation required."}
            result, mode = generate_json(f"Create high-level construction plan for {req.model_dump()}. Return JSON keys headline, phases objects phase/duration/tasks, milestones, risks, next_steps, limitations. Do not imply professional validation.", fallback)
            result.update(mode=mode, inputs=req.model_dump())
            report("plan", f"Plan — {name}", result)
        except Exception as e:
            st.error(f"Please check the inputs: {e}")

elif page == "Daily Assistance":
    with st.form("daily"):
        question = st.text_area("What do you need help with?")
        city = st.text_input("City (optional)")
        weather = st.text_input("Weather conditions", value="Not provided")
        stage = st.selectbox("Work stage", ["General site work","Foundation","Structure","Masonry","Electrical","Plumbing","Finishing","Roofing"])
        submit = st.form_submit_button("Get Guidance")
    if submit:
        try:
            req = DailyRequest(question=question, city=city, weather=weather, work_stage=stage)
            fallback = {"headline":"Daily site briefing",
                "answer":f"For {stage.lower()}, review approved drawings, permits, PPE, access and supervisor responsibilities.",
                "checklist":["Review method statement","Check PPE and equipment","Inspect access and housekeeping","Record hazards","Escalate imminent danger"],
                "weather_advice":"No live weather data is connected. Check a trusted local forecast.",
                "follow_up":"Share more site details for a tailored checklist.","limitations":"General guidance only."}
            result, mode = generate_json(f"Answer this construction site question safely: {req.model_dump()}. Return JSON keys headline, answer, checklist array, weather_advice, follow_up, limitations. Do not claim live weather access.", fallback)
            result.update(mode=mode, inputs=req.model_dump())
            report("daily_assistance", "Daily site assistance", result)
        except Exception as e:
            st.error(f"Please check the inputs: {e}")

elif page == "Analysis History":
    items = list_analyses(100)
    if not items:
        st.info("No saved reports yet.")
    for item in items:
        with st.expander(f"#{item['id']} · {item['title']} · {item['created_at']}"):
            st.write(item["summary"])
            st.json(item["result"])
