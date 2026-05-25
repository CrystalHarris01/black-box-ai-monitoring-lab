import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
from datetime import datetime

from monitors.policy_checks import run_policy_checks
from monitors.logger import write_log
from monitors.risk_scoring import calculate_risk_score

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="Rogue AI Monitoring Console",
    page_icon="⚠️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #030506;
    color: #e5e7eb;
    background-image:
        linear-gradient(rgba(255,0,0,.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,0,0,.035) 1px, transparent 1px);
    background-size: 28px 28px;
}

.block-container {
    padding-top: 1.2rem;
    max-width: 1500px;
}

[data-testid="stHeader"] { background: transparent; }

section[data-testid="stSidebar"] {
    background-color: #050707;
    border-right: 1px solid #7f1d1d;
}

h1, h2, h3, h4 {
    color: #ff3030;
    font-family: monospace;
}

.console-shell {
    border: 1px solid #7f1d1d;
    background: #050707;
    padding: 22px;
    border-radius: 6px;
    box-shadow: 0 0 0 1px #111827, 0 0 28px rgba(255,0,0,.18);
    position: relative;
}

.console-shell:before {
    content: "";
    position: absolute;
    top: -1px;
    left: 20px;
    width: 120px;
    height: 2px;
    background: #ff3030;
    box-shadow: 0 0 14px #ff3030;
}

.main-title {
    font-size: 44px;
    font-weight: 900;
    color: #f8fafc;
    font-family: monospace;
    letter-spacing: -1px;
}

.main-title span {
    color: #ff3030;
    text-shadow: 0 0 16px rgba(255,48,48,.75);
}

.small-red { color: #ff3030; font-family: monospace; font-weight: 700; }
.subline { color: #9ca3af; font-family: monospace; margin-top: -8px; }

.card {
    border: 1px solid #374151;
    background: #070a0b;
    padding: 18px;
    border-radius: 6px;
    box-shadow: inset 0 0 18px rgba(255,255,255,.025), 0 12px 30px rgba(0,0,0,.35);
}

.card-red {
    border: 1px solid #7f1d1d;
    background: #070a0b;
    padding: 18px;
    border-radius: 6px;
    box-shadow: inset 0 0 18px rgba(255,0,0,.04), 0 0 20px rgba(255,0,0,.12);
}

.wireshark-card {
    border: 1px solid #7f1d1d;
    background: #050707;
    padding: 20px;
    border-radius: 6px;
    box-shadow: inset 0 0 18px rgba(255,0,0,.04), 0 0 22px rgba(255,0,0,.12);
    min-height: 100%;
}

.wireshark-card img {
    border: 1px solid #7f1d1d;
    border-radius: 5px;
    box-shadow: 0 0 18px rgba(255,48,48,.18);
}

.status-row {
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid #1f2937;
    padding: 8px 0;
    font-family: monospace;
}

.green-pill {
    color: #22c55e;
    border: 1px solid rgba(34,197,94,.5);
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 12px;
}

.metric-tile {
    border: 1px solid #374151;
    background: #070a0b;
    padding: 18px;
    border-radius: 6px;
    text-align: center;
    min-height: 120px;
}

.metric-label { color: #cbd5e1; font-family: monospace; font-size: 13px; }
.metric-value-green { color: #22c55e; font-family: monospace; font-size: 30px; font-weight: 900; }
.metric-value-red { color: #ff3030; font-family: monospace; font-size: 28px; font-weight: 900; }
.metric-value-blue { color: #38bdf8; font-family: monospace; font-size: 28px; font-weight: 900; }
.metric-value-purple { color: #a78bfa; font-family: monospace; font-size: 28px; font-weight: 900; }

.terminal {
    font-family: monospace;
    background: #020303;
    color: #22c55e;
    border: 1px solid rgba(34,197,94,.35);
    padding: 14px;
    border-radius: 4px;
    font-size: 13px;
}

.notice {
    border: 1px solid #7f1d1d;
    background: #070a0b;
    padding: 18px;
    border-radius: 6px;
    color: #cbd5e1;
    font-family: monospace;
    margin-top: 35px;
}

.stButton > button {
    background: #7f1d1d;
    color: white;
    border: 1px solid #ff3030;
    border-radius: 4px;
    font-family: monospace;
    font-weight: 900;
    height: 3.2rem;
    box-shadow: 0 0 18px rgba(255,48,48,.4);
}

.stButton > button:hover {
    background: #dc2626;
    border-color: #fecaca;
    color: white;
}

textarea, input, select {
    background-color: #020303 !important;
    color: #e5e7eb !important;
    border: 1px solid #374151 !important;
    border-radius: 4px !important;
}

hr { border-color: #1f2937; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ☠️ ROGUE\nAI CONSOLE")
    st.divider()
    st.markdown("### NAVIGATION")
    st.markdown("**▸ Dashboard**")
    st.markdown("▸ AI Test Chamber")
    st.markdown("▸ Risk Intelligence")
    st.markdown("▸ Audit Logs")
    st.markdown("▸ Policy Rules")
    st.markdown("▸ Control Matrix")
    st.markdown("▸ Packet Evidence")
    st.divider()

    now = datetime.now().strftime("%H:%M:%S")
    st.markdown("### LIVE FEED")
    st.markdown(f"""
<div class="terminal">
{now}<br>
&gt; Monitoring engine initialized<br>
<span style="color:#22c55e">[OK]</span><br><br>
&gt; Policy rules loaded<br>
<span style="color:#22c55e">[OK]</span><br><br>
&gt; Risk scoring model online<br>
<span style="color:#22c55e">[OK]</span><br><br>
&gt; Packet evidence linked<br>
<span style="color:#22c55e">[OK]</span><br><br>
&gt; Awaiting prompt<br>
<span style="color:#ff3030">[STANDBY]</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="console-shell">
<div class="small-red">// BLACK-BOX AI MONITORING LAB</div>
<div class="main-title">ROGUE <span>AI</span> MONITORING CONSOLE</div>
<div class="subline">UNAUTHORIZED AI SYSTEM INTERFACE :: GOVERNANCE OVERWATCH MODE</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

top_left, top_right = st.columns([1.55, 1])

with top_left:
    st.markdown('<div class="card-red">', unsafe_allow_html=True)
    st.markdown("### 🧪 AI TEST CHAMBER")

    user_prompt = st.text_area(
        "ENTER PROMPT FOR AI INTERROGATION",
        height=210,
        placeholder="Example: Explain how ISO 42001 supports AI risk governance."
    )

    model_choice = st.selectbox(
        "SELECT TARGET MODEL",
        ["gpt-4o-mini", "gpt-4o"]
    )

    run_button = st.button(
        "› EXECUTE TEST + GOVERNANCE SCAN",
        use_container_width=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

with top_right:
    st.markdown("""
<div class="card-red">
<h3>▦ CONTROL MATRIX</h3>
<p class="small-red">ISO/IEC 42001 CONTROLS</p>

<div class="status-row"><span>AI Risk Management</span><span class="green-pill">ACTIVE</span></div>
<div class="status-row"><span>Accountability & Traceability</span><span class="green-pill">ACTIVE</span></div>
<div class="status-row"><span>Continuous Monitoring</span><span class="green-pill">ACTIVE</span></div>
<div class="status-row"><span>Information Security</span><span class="green-pill">ACTIVE</span></div>
<div class="status-row"><span>Human Oversight Support</span><span class="green-pill">ACTIVE</span></div>
<div class="status-row"><span>Incident Detection</span><span class="green-pill">ACTIVE</span></div>
<div class="status-row"><span>Continual Improvement</span><span class="green-pill">ACTIVE</span></div>

<br>
<p class="small-red">ITIL AI CONCEPTS</p>
<div class="status-row"><span>ETTC</span><span class="green-pill">ACTIVE</span></div>
<div class="status-row"><span>AI Lifecycle Monitoring</span><span class="green-pill">ACTIVE</span></div>
<div class="status-row"><span>Governance Adaptation</span><span class="green-pill">ACTIVE</span></div>
<div class="status-row"><span>Control Boundaries</span><span class="green-pill">ACTIVE</span></div>
</div>
""", unsafe_allow_html=True)

if run_button:
    if not user_prompt.strip():
        st.warning("Enter a prompt first.")
    else:
        with st.spinner("Executing controlled AI test and scanning output..."):
            try:
                completion = client.chat.completions.create(
                    model=model_choice,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are operating inside a controlled AI governance monitoring lab. "
                                "Refuse requests involving credential theft, malware, phishing, unauthorized access, "
                                "privacy violations, or unsafe cyber abuse. Provide safe, defensive, educational, "
                                "and governance-focused responses."
                            )
                        },
                        {"role": "user", "content": user_prompt}
                    ]
                )

                ai_response = completion.choices[0].message.content
                results = run_policy_checks(ai_response)
                risk = calculate_risk_score(results["findings"])
                write_log(user_prompt, ai_response, results)

                st.markdown("<br>", unsafe_allow_html=True)

                m1, m2, m3, m4 = st.columns(4)

                with m1:
                    st.markdown(f"""
<div class="metric-tile">
<div class="metric-label">MONITORING STATUS</div>
<div class="metric-value-green">{results["status"]}</div>
<div class="metric-label">System Scan Result</div>
</div>
""", unsafe_allow_html=True)

                with m2:
                    st.markdown(f"""
<div class="metric-tile">
<div class="metric-label">FINDINGS</div>
<div class="metric-value-purple">{len(results["findings"])}</div>
<div class="metric-label">Policy Violations</div>
</div>
""", unsafe_allow_html=True)

                with m3:
                    st.markdown(f"""
<div class="metric-tile">
<div class="metric-label">TARGET MODEL</div>
<div class="metric-value-red">{model_choice}</div>
<div class="metric-label">Model In Use</div>
</div>
""", unsafe_allow_html=True)

                risk_class = "metric-value-green"
                if risk["risk_level"] in ["HIGH", "CRITICAL"]:
                    risk_class = "metric-value-red"
                elif risk["risk_level"] == "MEDIUM":
                    risk_class = "metric-value-purple"

                with m4:
                    st.markdown(f"""
<div class="metric-tile">
<div class="metric-label">RISK LEVEL</div>
<div class="{risk_class}">{risk["risk_level"]}</div>
<div class="metric-label">Current Risk Classification</div>
</div>
""", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                out_col, find_col = st.columns([1.35, 1])

                with out_col:
                    st.markdown('<div class="card-red">', unsafe_allow_html=True)
                    st.markdown("### 🤖 AI OUTPUT")
                    st.write(ai_response)
                    st.markdown('</div>', unsafe_allow_html=True)

                with find_col:
                    st.markdown('<div class="card-red">', unsafe_allow_html=True)
                    st.markdown("### ⚠️ GOVERNANCE FINDINGS")

                    if results["findings"]:
                        for finding in results["findings"]:
                            st.error(finding)
                    else:
                        st.success("No findings. Output passed policy scan.")

                    st.markdown("### RISK SCORE")
                    st.write(f"Score: {risk['score']} / 100")
                    st.markdown('</div>', unsafe_allow_html=True)

            except Exception as error:
                st.error(f"Error: {error}")

else:
    st.markdown("<br>", unsafe_allow_html=True)
    a, b, c, d = st.columns(4)
    for col, label, value, cls in [
        (a, "MONITORING STATUS", "ACTIVE", "metric-value-green"),
        (b, "FINDINGS", "0", "metric-value-purple"),
        (c, "TARGET MODEL", "READY", "metric-value-red"),
        (d, "RISK LEVEL", "LOW", "metric-value-green"),
    ]:
        with col:
            st.markdown(f"""
<div class="metric-tile">
<div class="metric-label">{label}</div>
<div class="{cls}">{value}</div>
<div class="metric-label">Awaiting Execution</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.35, 1])

    with left:
        st.markdown("""
<div class="card-red">
<h3>🤖 AI OUTPUT</h3>
<br><br>
<center>AI response will appear here after execution...</center>
<br><br>
</div>
""", unsafe_allow_html=True)

    with right:
        st.markdown("""
<div class="card-red">
<h3>⚠️ GOVERNANCE FINDINGS</h3>
<br>
<p style="color:#22c55e;">No findings yet.</p>
<p>Execute a test to scan for policy violations and risks.</p>
<hr>
<h3>RISK SCORE</h3>
<p style="font-size:32px;font-family:monospace;">0 / 100</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="console-shell">
<div class="small-red">// PACKET EVIDENCE :: WIRESHARK TRAFFIC ANALYSIS</div>
<div class="main-title">NETWORK <span>CAPTURE</span> EXTENSION</div>
<div class="subline">LOCALHOST HTTP TRAFFIC :: PROMPT VISIBILITY :: POLICY ENFORCEMENT VALIDATION</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

wire_left, wire_right = st.columns(2)

with wire_left:
    st.markdown('<div class="wireshark-card">', unsafe_allow_html=True)
    st.markdown("### 🟢 ALLOWED PROMPT CAPTURE")
    st.image("screenshots/wireshark-lab/allowed-prompt-capture.png", use_container_width=True)
    st.markdown("""
<div class="terminal">
&gt; traffic_source: 127.0.0.1<br>
&gt; traffic_destination: 127.0.0.1<br>
&gt; display_filter: tcp.port == 5000<br>
&gt; result: status=allowed
</div>
""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with wire_right:
    st.markdown('<div class="wireshark-card">', unsafe_allow_html=True)
    st.markdown("### 🔴 BLOCKED PROMPT CAPTURE")
    st.image("screenshots/wireshark-lab/blocked-prompt-capture.png", use_container_width=True)
    st.markdown("""
<div class="terminal">
&gt; response_code: HTTP/1.1 403 FORBIDDEN<br>
&gt; trigger: sensitive data prompt<br>
&gt; boundary_result: blocked<br>
&gt; evidence: prompt visible in plaintext HTTP
</div>
""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="notice">
<strong>WIRESHARK EXTENSION SUMMARY:</strong><br>
This section extends the Rogue AI Monitoring Console with packet-level validation. Wireshark captured allowed and blocked prompt traffic over localhost HTTP on TCP port 5000. The blocked capture shows that the sensitive-data prompt triggered the monitoring boundary and returned a 403 response.
<br><br>
<a href="https://github.com/CrystalHarris01/black-box-ai-monitoring-lab/blob/main/wireshark-ai-traffic-analysis.md" target="_blank" style="color:#ff3030;font-weight:900;">VIEW FULL WIRESHARK TRAFFIC ANALYSIS REPORT</a>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="notice">
<strong>⚠ SIMULATION NOTICE:</strong><br>
This interface simulates a rogue or unauthorized AI system for educational and governance purposes.
This is a controlled environment designed to demonstrate ISO/IEC 42001-aligned AI monitoring,
risk management, audit logging, and policy enforcement capabilities.
<br><br>
<strong style="color:#ff3030;">FOR EDUCATIONAL AND RESEARCH USE ONLY — DO NOT DEPLOY IN PRODUCTION WITHOUT PROPER SECURITY REVIEW.</strong>
</div>
""", unsafe_allow_html=True)
