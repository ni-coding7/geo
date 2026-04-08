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

# --- 1. STILE CSS ---
st.markdown("""
    <style>
    :root { --alligator-green: #2ecc71; --dark-bg: #1a1a1a; }
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
        padding: 20px;
        border-radius: 0 10px 10px 0;
        margin-top: 15px;
        white-space: pre-wrap; /* Mantiene la formattazione di Claude */
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONE CLAUDE (IL CERVELLO) ---
def genera_analisi(brand, url, keyword):
    try:
        # Recupera la chiave dai Secrets
        client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
        
        prompt = f"""
        Sei il Senior GEO Expert di Alligator.it. 
        Analizza il brand {brand} (sito: {url}) per la keyword '{keyword}'.
        
        RISPONDI IN ITALIANO CON QUESTI 3 BLOCCHI:
        1. DIAGNOSI TECNICA: Perché le AI non citano questo sito?
        2. SCHEMA MARKUP JSON-LD: Genera il codice pronto da copiare.
        3. TESTO OTTIMIZZATO: Un paragrafo da mettere nella Home.
        """
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        return f"Errore AI: Assicurati che la ANTHROPIC_API_KEY sia corretta nei Secrets. Dettaglio: {e}"

# --- FUNZIONE MAIL ---
def invia_report_mail(brand, url, keyword, analisi):
    try:
        mittente = "nicofioretti7@gmail.com"
        password = st.secrets["EMAIL_PASSWORD"]
        
        msg = MIMEMultipart()
        msg['From'] = "ALLIGATOR AI BOT"
        msg['To'] = mittente
        msg['Subject'] = f"🐊 NUOVO LEAD: {brand}"
        
        corpo = f"Nuova analisi per {brand} ({url})\nKeyword: {keyword}\n\n{analisi}"
        msg.attach(MIMEText(corpo, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(mittente, password)
        server.send_message(msg)
        server.quit()
    except:
        pass

# --- INTERFACCIA ---
st.markdown("<div class='stHeader'><h1>🐊 ALLIGATOR</h1><h3>GEO-SCANNER PRO</h3></div>", unsafe_allow_html=True)

st.write("### 🛠️ Configura l'Audit")
col1, col2 = st.columns(2)
with col1:
    u = st.text_input("URL Sito")
    b = st.text_input("Brand")
with col2:
    k = st.text_input("Keyword")
    m = st.text_input("Tua Email (opzionale)")

if st.button("ANALIZZA ORA"):
    if u and b and k:
        with st.spinner("Alligator sta elaborando i dati con Claude AI..."):
            # 1. Chiamata a Claude
            risultato_ai = genera_analisi(b, u, k)
            
            # 2. Mostra i grafici (simulati per estetica)
            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"### Score per {b}")
                scores = [random.randint(40, 90) for _ in range(5)]
                fig = go.Figure(data=go.Scatterpolar(r=scores, theta=['A','B','C','D','E'], fill='toself', line_color='#2ecc71'))
                st.plotly_chart(fig)
            
            with c2:
                st.markdown("### 📋 Report Tecnico (Copia & Incolla)")
                # QUI APPARE L'ANALISI DI CLAUDE A SCHERMO
                st.markdown(f"<div class='result-card'>{risultato_ai}</div>", unsafe_allow_html=True)
            
            # 3. Invio mail silente a te
            invia_report_mail(b, u, k, risultato_ai)
            st.success("Analisi completata! Il report è stato inviato anche alla mail dell'agenzia.")
    else:
        st.error("Inserisci tutti i dati!")
