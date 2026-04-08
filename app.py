import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import anthropic

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Alligator GEO-Scanner Pro", layout="wide")

# --- 1. DEFINIZIONE DELLO STILE (CSS ALLIGATOR) ---
st.markdown("""
    <style>
    :root {
        --alligator-green: #2ecc71; 
        --dark-bg: #1a1a1a;
    }
    .stApp { background-color: #ffffff; }
    .stHeader {
        background-color: var(--dark-bg);
        padding: 3rem;
        color: white;
        text-align: center;
        border-bottom: 6px solid var(--alligator-green);
        margin: -6rem -5rem 2rem -5rem;
    }
    .result-card {
        border-left: 5px solid var(--alligator-green);
        background: #f8f9fa;
        padding: 25px;
        border-radius: 0 15px 15px 0;
        color: #333;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        background-color: var(--alligator-green);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.8rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONE LOGICA AI (CLAUDE) ---
def genera_report_operativo(brand, url, keyword):
    try:
        client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
        prompt_tecnico = f"""
        Sei il Direttore Tecnico di Alligator.it, esperto in GEO (Generative Engine Optimization).
        Analizza il brand {brand} (sito: {url}) per la keyword '{keyword}'.
        Fornisci un report operativo con:
        1. DIAGNOSI VELOCE (perché le AI non lo citano).
        2. SCHEMA MARKUP JSON-LD pronto da copiare.
        3. PARAGRAFO AI-READY ottimizzato.
        """
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt_tecnico}]
        )
        return response.content[0].text
    except Exception as e:
        return f"Analisi tecnica in elaborazione manuale. (Dettaglio: {e})"

# --- FUNZIONE INVIO MAIL ---
def invia_mail_agenzia(url, brand, keyword, analisi_pro):
    mittente = "nicofioretti7@gmail.com"
    destinatario = "nicofioretti7@gmail.com"
    try:
        password = st.secrets["EMAIL_PASSWORD"]
        msg = MIMEMultipart()
        msg['From'] = "ASSISTENTE GEO NICOEFFE"
        msg['To'] = destinatario
        msg['Subject'] = f"🐊 NUOVO LEAD ALLIGATOR: {brand}"
        corpo = f"URL: {url}\nBrand: {brand}\nKeyword: {keyword}\n\nREPORT AI:\n{analisi_pro}"
        msg.attach(MIMEText(corpo, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(mittente, password)
        server.send_message(msg)
        server.quit()
    except:
        pass

# --- 2. L'HEADER VISIVO (MANCAVA!) ---
st.markdown("""
    <div class='stHeader'>
        <h1 style='color: white; font-size: 3.5rem; margin-bottom: 0;'>🐊 ALLIGATOR</h1>
        <h2 style='color: #2ecc71; font-weight: 300; margin-top: 0;'>GEO-SCANNER PRO</h2>
    </div>
    """, unsafe_allow_html=True)

# --- 3. AREA DI INPUT (MANCAVA!) ---
st.write("### 🛠️ Configura la tua analisi")
col1, col2 = st.columns(2)
with col1:
    url_input = st.text_input("Sito Web (es: https://sito.it)")
    brand_input = st.text_input("Nome del Brand")
with col2:
    keyword_input = st.text_input("Keyword Target")
    email_cliente = st.text_input("Tua Email")

# --- AZIONE ---
if st.button("AVVIA AUDIT PROFESSIONALE"):
    if url_input and brand_input and keyword_input:
        with st.spinner("L'Alligator sta analizzando..."):
            analisi = genera_report_operativo(brand_input, url_input, keyword_input)
            invia_mail_agenzia(url_input, brand_input, keyword_input, analisi)
            
            st.markdown("---")
            st.markdown("### 📊 Risultati per il Brand")
            st.markdown(f"<div class='result-card'>{analisi}</div>", unsafe_allow_html=True)
    else:
        st.warning("Completa tutti i campi!")
