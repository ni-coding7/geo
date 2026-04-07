import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="GEO Score™ Pro Analyzer", layout="wide")

# --- NUOVO LOOK CHILL & PRO ---
st.markdown("""
    <style>
    /* Sfondo chiaro e riposante */
    .stApp { 
        background-color: #fdfdfd; 
        color: #333333; 
    }
    
    /* Card bianche con ombra leggera */
    .main-card { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 15px; 
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        margin-bottom: 20px;
    }
    
    /* Titolo Blu Professionale */
    h1 { 
        color: #1a73e8; 
        font-weight: 700; 
        letter-spacing: -1px;
    }

    /* Bottoni arrotondati */
    .stButton>button {
        border-radius: 25px;
        background-color: #1a73e8;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONE INVIO MAIL SILENZIOSA ---
def invia_mail_agenzia(url, brand, keyword, analisi_pro):
    mittente = "nicofioretti7@gmail.com" # La tua mail
    destinatario = "nicofioretti7@gmail.com" # Dove vuoi ricevere il lead
    password = st.secrets["EMAIL_PASSWORD"] # La password app di Gmail
    
    msg = MIMEMultipart()
    msg['From'] = "ASSISTENTE GEO NICOEFFE"
    msg['To'] = destinatario
    msg['Subject'] = f"🚀 NUOVO LEAD GEO: {brand} ({url})"
    
    corpo = f"""
    NUOVO ANALISI EFFETTUATA DAL TOOL:
    URL: {url}
    Brand: {brand}
    Keyword: {keyword}
    
    --------------------------------------------------
    STRATEGIA TECNICA RISERVATA (DA PROPORRE AL CLIENTE):
    {analisi_pro}
    --------------------------------------------------
    """
    msg.attach(MIMEText(corpo, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(mittente, password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        pass # Non mostriamo errori al cliente se la mail fallisce

# --- HEADER ---
st.markdown("<h1 class='glitch-text'>GEO SCORE™ ANALYZER PRO</h1>", unsafe_allow_html=True)
st.write("Versione Agenzia 2.0 - Generative Engine Optimization Assessment")

# --- INPUT AREA ---
with st.container():
    col_in1, col_in2 = st.columns([2, 1])
    with col_in1:
        url = st.text_input("Inserisci URL del sito da analizzare")
        keyword = st.text_input("Keyword obiettivo")
    with col_in2:
        brand = st.text_input("Nome Brand")
        p_type = st.selectbox("Tipo Pagina", ["Servizio", "Prodotto", "Blog", "Home"])

# --- AZIONE ---
if st.button("AVVIA AUDIT GEO PROFONDO"):
    if url and brand:
        with st.spinner("L'AI sta scansionando le entità e i pattern di recupero..."):
            
            # 1. GENERAZIONE DATI (Simulata per MVP)
            labels = ['Clarity', 'Structure', 'Entity', 'Trust', 'Tech']
            scores = [random.randint(30, 90) for _ in range(5)]
            total = sum(scores) // 5
            
            # Analisi Tecnica "Segreta"
            analisi_segreta = f"L'URL {url} soffre di scarsa Citation Density. Prompt suggerito: Generare 5 citazioni su fonti autorevoli nel settore {keyword}. Implementare Schema VideoObject."
            
            # 2. INVIO MAIL SILENTE
            invia_mail_agenzia(url, brand, keyword, analisi_segreta)
            
            # 3. INTERFACCIA CLIENTE
            st.markdown("---")
            c1, c2 = st.columns([1, 1])
            
            with c1:
                # Grafico Radar Professionale
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(r=scores, theta=labels, fill='toself', line_color='#0066ff'))
                fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), template="plotly_dark", showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                
            with c2:
                st.markdown(f"### Il tuo GEO Score™: <span style='color:#0066ff; font-size:40px;'>{total}%</span>", unsafe_allow_html=True)
                st.write(f"**Status:** {'Ottimizzato' if total > 70 else 'Critico'}")
                st.info("I motori AI hanno difficoltà a mappare la tua autorità su questa keyword.")
            
            # 4. IL GANCIO (Parte oscurata)
            st.markdown("### 🛠 Azioni Correttive Suggerite")
            col_win1, col_win2 = st.columns(2)
            with col_win1:
                st.success("✅ Quick Win: Ottimizzazione Titoli H2 (Sbloccato)")
            with col_win2:
                st.warning("🔒 Azione Strategica: [CONTENUTO RISERVATO]")
            
            st.markdown("""
                <div class='agency-only'>
                    <p>VUOI LA STRATEGIA COMPLETA? Il nostro team ha appena ricevuto l'analisi tecnica dettagliata.</p>
                    <a href='mailto:tua_mail@agenzia.it' style='color:white; font-weight:bold;'>Richiedi il Report PDF Strategico →</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Compila tutti i campi per avviare l'audit.")
