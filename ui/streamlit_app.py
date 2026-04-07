import os, time, requests, streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:5000")

st.set_page_config(page_title="BMW Price Predictor", page_icon="🚗", layout="wide")
st.title("BMW Price Predictor")
st.caption("Single-car estimate. Inputs are validated and standardized to match the model.")

# ---- optional styling ----
st.markdown("""
<style>
div[data-testid="stForm"] {border: 1px solid #1f2937; border-radius: 14px; padding: 1rem 1rem 0.5rem;}
.result-card { background: #0f1b2d; border: 1px solid #1f2937; padding: 14px 18px; border-radius: 12px; }
.small { color:#94a3b8; font-size:0.9rem }
</style>
""", unsafe_allow_html=True)

# Fixed, known-good options so casing/typos can’t happen
MODEL_OPTIONS = [
    "1 Series","2 Series","3 Series","4 Series","5 Series",
    "X1","X2","X3","X4","X5","X6","7 Series","8 Series"
]
TRANSMISSION_OPTIONS = ["Automatic","Manual","Semi-Auto"]
FUEL_OPTIONS = ["Diesel","Petrol","Hybrid"]
ENGINE_OPTIONS = [1.0,1.5,1.6,1.9,2.0,3.0,3.5,4.0,4.4,5.0,6.6]

with st.form("predict_form", clear_on_submit=False):
    c1, c2 = st.columns(2)
    with c1:
        model = st.selectbox("Model", MODEL_OPTIONS, index=2)
        year = st.number_input("Year", min_value=1996, max_value=2025, value=2018, step=1)
        transmission = st.selectbox("Transmission", TRANSMISSION_OPTIONS, index=0)
        fuelType = st.selectbox("Fuel Type", FUEL_OPTIONS, index=0)
    with c2:
        mileage = st.number_input("Mileage", min_value=0, max_value=300000, value=30000, step=500)
        tax = st.number_input("Tax (£/yr)", min_value=0, max_value=600, value=145, step=5)
        mpg = st.number_input("MPG", min_value=5.0, max_value=100.0, value=55.0, step=0.1)
        engineSize = st.selectbox("Engine Size (L)", ENGINE_OPTIONS, index=4)

    submitted = st.form_submit_button("Predict", use_container_width=True)

if submitted:
    # Build safe payload (no casing issues; FastAPI already strips & validates)
    payload = {
        "model": model,                    # comes from dropdown (valid casing)
        "year": int(year),
        "transmission": transmission,      # dropdown
        "mileage": int(mileage),
        "fuelType": fuelType,              # dropdown
        "tax": int(tax),
        "mpg": float(mpg),
        "engineSize": float(engineSize),
    }

    # simple client-side guards mirroring backend ranges
    errors = []
    if not (1990 <= payload["year"] <= 2025): errors.append("Year out of range.")
    if payload["mileage"] < 0: errors.append("Mileage must be ≥ 0.")
    if not (5 <= payload["mpg"] <= 100): errors.append("MPG must be in [5,100].")
    if not (1.0 <= payload["engineSize"] <= 6.6): errors.append("Engine size must be in [1.0,6.6].")
    if errors:
        for e in errors: st.error(e)
    else:
        with st.spinner("Crunching the numbers…"):
            t0 = time.time()
            r = requests.post(f"{API_URL}/bmw_predict_price", json=payload, timeout=20)
            latency_ms = int((time.time() - t0) * 1000)

        if r.ok:
            price = r.json().get("predicted_price")
            st.markdown(
                f"""<div class='result-card'>
                    <h4>Estimated price</h4>
                    <h2>💵 ${price:,.0f}</h2>
                    <div class='small'>Latency: {latency_ms} ms • Model: XGBoost</div>
                </div>""",
                unsafe_allow_html=True
            )
        else:
            st.error(f"API error {r.status_code}: {r.text}")

with st.sidebar:
    st.subheader("ℹ️ Notes")
    st.write("- Inputs are constrained to valid choices used during training.")
    st.write("- If you deploy the API/UI separately, set `API_URL` env variable.")
    st.divider()
    st.code(f"API_URL={API_URL}", language="bash")