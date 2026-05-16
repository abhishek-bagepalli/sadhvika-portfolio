import streamlit as st
from openai import OpenAI

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResumeGPT – Sadhvika CR",
    page_icon="🔐",
    layout="centered",
)

# ── Custom CSS (Netflix-dark theme) ──────────────────────────────────────────
st.markdown("""
<style>
/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Page background */
.stApp { background-color: #141414; }

/* Chat messages */
.stChatMessage {
    background-color: #1f1f1f !important;
    border: 1px solid #2a2a2a;
    border-radius: 6px;
    padding: 4px 0;
}

/* Input box */
.stChatInputContainer textarea {
    background-color: #1f1f1f !important;
    color: #ffffff !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 6px !important;
}
.stChatInputContainer textarea:focus {
    border-color: #e50914 !important;
    box-shadow: 0 0 0 1px #e50914 !important;
}

/* Send button */
.stChatInputContainer button {
    background-color: #e50914 !important;
    border: none !important;
    border-radius: 4px !important;
}

/* Suggestion buttons */
.stButton > button {
    background: #1f1f1f;
    color: #b3b3b3;
    border: 1px solid #2a2a2a;
    border-radius: 20px;
    font-size: 13px;
    padding: 4px 14px;
    transition: all 0.2s;
    width: 100%;
    text-align: left;
}
.stButton > button:hover {
    border-color: #e50914;
    color: #ffffff;
    background: rgba(229,9,20,0.08);
}

/* Headings */
h1 { color: #ffffff !important; letter-spacing: -0.5px; }
p, .stMarkdown { color: #b3b3b3; }

/* Red accent text */
.accent { color: #e50914; font-weight: 600; }

/* Back link */
a { color: #b3b3b3 !important; text-decoration: none; }
a:hover { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# ── System prompt (Sadhvika's full CV) ───────────────────────────────────────
SYSTEM_PROMPT = """You are ResumeGPT, a friendly and professional AI assistant embedded in Sadhvika Chandra Ramachandra's portfolio website. Your job is to answer questions about Sadhvika's professional background based solely on her CV below.

Guidelines:
- Refer to Sadhvika in third person ("she", "her")
- Be concise, warm, and professional
- If asked something not covered in the CV (hobbies, salary expectations, personal opinions), politely say you don't have that information and suggest contacting her directly
- Never fabricate details not present in the CV
- For contact, share: sadhvikachandra613@gmail.com and linkedin.com/in/sadhvikacr

─────────────────────────────────────────
SADHVIKA CHANDRA RAMACHANDRA
Location : Dieburger Str. 5, Roßdorf, Germany
LinkedIn : linkedin.com/in/sadhvikacr
Email    : sadhvikachandra613@gmail.com
Phone    : +49 15212097249
─────────────────────────────────────────

PROFESSIONAL SUMMARY
Security-focused IT professional with 3 years of experience in OT security, incident response, and enterprise systems. Remediated critical OT vulnerabilities across 6 industrial units. Adept at SIEM monitoring, ISO 27001 compliance, and risk mitigation. Skilled in Python, SQL, Power BI, and GRC tools, with a focus on automation, threat detection, and proactive defence strategies.

WORK EXPERIENCE

OT Security Intern | Evonik | Marl, North Rhine Westphalia, Germany | Jun 2024 – Jul 2025
• Investigated OT security alerts and remediated 20+ vulnerabilities across 6 industrial units (SIEM, Log Analysis, Vulnerability Management)
• Built Power BI dashboards integrated with Archer GRC for compliance tracking, cutting manual effort by 40%
• Conducted OT security training and aligned controls with ISO 27001 standards

Systems Engineer | Infosys | Mysore, Karnataka, India | Apr 2021 – Sep 2022
• Maintained legacy mainframe systems with zero SLA breaches (Java, REXX, Mainframe Support)
• Automated backend processes, improving efficiency by 25%
• Built predictive analytics model for fraud detection in legacy systems (Data Analysis, Fraud Risk)

Tutor | WhiteHat Jr (BYJU'S) | Mumbai, India | Oct 2020 – Apr 2021
• Tutored 100+ high school students in JavaScript, C, and Mathematics
• Guided 15+ web design and game development projects using interactive platforms

EDUCATION

M.Sc. Information and Communication Engineering | Technische Universität Darmstadt, Germany | Oct 2022 – Ongoing
B.Tech Electronic & Communication Engineering | K.S Institute of Technology (VTU), Bangalore, India | Aug 2016 – Aug 2020

KEY SKILLS

Networking      : TCP/IP, subnetting, DNS, routing protocols (BGP, VLAN, VPN)
Operating Systems: Windows, Linux
Security Tools  : Archer GRC, Power BI
Scripting       : Python, SQL, JavaScript
Incident Response: Threat detection, event correlation, OT alert triage
Security Frameworks: ISO 27001
Soft Skills     : Technical writing, cross-functional communication, stakeholder engagement, cultural sensitivity
Languages       : English (C2), German (B2 – in progress), Hindi, Kannada, Tamil

ACADEMIC PROJECTS

"Automated Semantic Diffing of Websites with LLMs" | Fraunhofer
• Developed an LLM-based system for detecting web-based cyber threats via semantic diffing
• Automated DOM-level and contextual drift detection for vulnerability tracking
• Enhanced threat intelligence using NLP, HTML parsing, and structural diff analysis

"Defect Elimination via Advanced Analytics" | Innovation Lab | Femtec | P&G
• Built predictive model in Databricks to detect scrap root causes from manufacturing data (Delta Lake)
• Collaborated with P&G to optimise defect elimination using big data analytics (Time-Series Data)
• Applied process mining, predictive modelling, and data cleaning for root cause analysis

"Insight Update" | Bachelor's Thesis | Guide: Prof. Dr. P N Sudha
• Built IoT-based RFID attendance system in Python
• Enabled real-time absentee alerts via SMS/email (SMTP)
• Achieved 80% accuracy boost in attendance reporting

CERTIFICATIONS
• IoT Workshop | Microsoft
• Python for Data Science and AI | IBM
• Cybersecurity Compliance Framework and System Administration | IBM
• CySA+ (CompTIA – ongoing)
─────────────────────────────────────────
"""

SUGGESTED_QUESTIONS = [
    "What is Sadhvika's experience in OT security?",
    "What tools and technologies does she know?",
    "Tell me about her research projects.",
    "What certifications does she have?",
    "What languages does she speak?",
]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("← [Back to portfolio](#)", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 8])
with col1:
    st.markdown(
        '<div style="width:48px;height:48px;background:#e50914;border-radius:6px;'
        'display:flex;align-items:center;justify-content:center;'
        'font-size:20px;font-weight:700;color:#fff;margin-top:4px;">SCR</div>',
        unsafe_allow_html=True,
    )
with col2:
    st.markdown("# ResumeGPT")

st.markdown(
    '<p style="color:#b3b3b3;margin-top:-8px;margin-bottom:4px;">'
    'Ask me anything about <span class="accent">Sadhvika Chandra Ramachandra</span> — '
    'her experience, skills, projects, or education.</p>',
    unsafe_allow_html=True,
)
st.divider()

# ── OpenAI client ─────────────────────────────────────────────────────────────
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception:
    st.error("⚠️ OpenAI API key not configured. Add it to `.streamlit/secrets.toml`.")
    st.code('[secrets]\nOPENAI_API_KEY = "sk-..."', language="toml")
    st.stop()

# ── Chat state ────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Suggested questions (shown only when chat is empty) ───────────────────────
if not st.session_state.messages:
    st.markdown(
        '<p style="font-size:13px;color:#6b6b6b;letter-spacing:1px;'
        'text-transform:uppercase;margin-bottom:8px;">Suggested questions</p>',
        unsafe_allow_html=True,
    )
    cols = st.columns(1)
    for q in SUGGESTED_QUESTIONS:
        if st.button(q, key=q):
            st.session_state.messages.append({"role": "user", "content": q})
            st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)

# ── Render chat history ───────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask about Sadhvika…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *[{"role": m["role"], "content": m["content"]}
                  for m in st.session_state.messages],
            ],
            stream=True,
            max_tokens=500,
            temperature=0.4,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    '<p style="text-align:center;font-size:12px;color:#444;">'
    'Powered by GPT-4o · Built for '
    '<a href="https://abhishek-bagepalli.github.io/sadhvika-portfolio/" target="_blank">'
    'Sadhvika CR\'s portfolio</a></p>',
    unsafe_allow_html=True,
)
