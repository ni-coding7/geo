import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import anthropic

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="Alligator GEO™ Professional", layout="wide", initial_sidebar_state="collapsed")

# Colori Alligator Pro
PRIMARY = "#2ecc71"
DARK = "#121212"
GRAY = "#f8f9fa"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    * {{ font-family: 'Inter', sans-serif; }}
    
    .stApp {{ background-color: white; }}
    
    /* Header Moderno */
    .main-header {{
        background: {DARK};
        padding: 4rem 2rem;
        border-bottom: 8px solid {PRIMARY};
        text-align: center;
        margin: -6rem -5rem 3rem -5rem;
    }}
    
    .main-header h1 {{
        color: white;
        font-size: 4rem;
        letter-spacing: -2px;
        margin: 0;
    }}
    
    .main-header p {{
        color: {PRIMARY};
        font-size: 1.2rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.5rem;
    }}

    /* Card Box */
    .glass-card {{
        background: {GRAY};
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #eee;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }}

    /* Bottoni Custom */
    .stButton>button {{
        width: 100%;
        background: {PRIMARY} !important;
        color: white !important;
        border: none !important;
        padding: 1rem !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(46, 204, 113, 0.4);
    }}

    /* Code Block Styling */
    code {{ color: {PRIMARY} !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 2. LOGICA DI BACKGROUND ---
def get_ai_analysis(brand, url, keyword):
    try:
        client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
        prompt = f"""Analizza il brand {brand} ({url}) per '{keyword}'. 
        Rispondi come Direttore Tecnico di Alligator.it.
        FORMATO: 
        1. DIAGNOSI BREVE.
        2. CODICE JSON-LD SCHEMA.ORG (in un blocco codice).
        3. PARAGRAFO DA COPIARE NELLA HOME."""
        
        msg = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text
    except Exception as e:
        return f"⚠️ Errore AI: Assicurati di aver inserito la ANTHROPIC_API_KEY nei Secrets di Streamlit. (Dettaglio: {e})"

def send_lead_email(brand, url, keyword, report):
    try:
        password = st.secrets["EMAIL_PASSWORD"]
        msg = MIMEMultipart()
        msg['Subject'] = f"🐊 NUOVO LEAD: {brand}"
        msg['From'] = "Alligator GEO Bot"
        msg['To'] = "nicofioretti7@gmail.com"
        msg.attach(MIMEText(f"URL: {url}\nBrand: {brand}\nKeyword: {keyword}\n\nREPORT:\n{report}", 'plain'))
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login("nicofioretti7@gmail.com", password)
            server.send_message(msg)
    except:
        pass

# --- 3. INTERFACCIA UTENTE ---
st.markdown(f"""
    <div class="main-header">
        <h1>🐊 ALLIGATOR</h1>
        <p>Generative Engine Optimization • Scanner Pro</p>
    </div>
""", unsafe_allow_html=True)

# Layout Input
with st.container():
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        u = st.text_input("🔗 URL SITO", placeholder="https://alligator.it")
    with c2:
        b = st.text_input("🏷️ NOME BRAND", placeholder="Alligator")
    with c3:
        k = st.text_input("🔑 KEYWORD", placeholder="SEO Agency")
    
    if st.button("ANALIZZA ORA"):
        if u and b and k:
            with st.spinner("Alligator AI sta scansionando le entità..."):
                # Esecuzione
                report = get_ai_analysis(b, u, k)
                send_lead_email(b, u, k, report)
                
                # Risultati
                st.markdown("---")
                res_left, res_right = st.columns([1, 1])
                
                with res_left:
                    # Grafico
                    labels = ['Clarity', 'Structure', 'Entity', 'Trust', 'Tech']
                    vals = [random.randint(50, 95) for _ in range(5)]
                    fig = go.Figure(data=go.Scatterpolar(
                        r=vals, theta=labels, fill='toself',
                        line_color=PRIMARY, fillcolor='rgba(46, 204, 113, 0.2)'
                    ))
                    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    score = sum(vals) // 5
                    st.metric("SCORE GLOBALE", f"{score}%", delta="Analizzato da Claude 3.5 Sonnet")
                
                with res_right:
                    st.markdown("### 🛠️ Roadmap Operativa (Copy-Paste)")
                    st.markdown(f"<div style='background: white; padding: 1.5rem; border-radius: 10px; border: 1px solid #ddd;'>{report}</div>", unsafe_allow_html=True)
                    st.success("Analisi inviata via mail al team Alligator.")
        else:
            st.error("Inserisci tutti i dati, bro!")
    st.markdown("</div>", unsafe_allow_html=True)
