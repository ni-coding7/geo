import streamlit as st
import pandas as pd
import random

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="GEO Score Tool | Analisi AI Visibility",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- STILE CSS PERSONALIZZATO (Look Premium & Agency) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .result-card { background-color: #ffffff; padding: 25px; border-radius: 15px; border-left: 5px solid #007bff; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
    .score-big { font-size: 48px; font-weight: 800; color: #007bff; }
    .status-badge { padding: 5px 15px; border-radius: 20px; font-size: 14px; font-weight: 600; }
    hr { margin: 2rem 0; opacity: 0.1; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGICA DI CALCOLO SIMULATA (MVP) ---
def calculate_geo_logic(url, page_type, keyword, brand):
    # Generiamo punteggi verosimili basati sulla completezza dei campi
    base = 50
    if len(url) > 10: base += 5
    if keyword: base += 10
    if brand: base += 10
    
    # Sottoscore (0-20 ciascuno)
    scores = {
        "Content Clarity": random.randint(12, 18),
        "Structure & Retrieval": random.randint(10, 19),
        "Entity & Brand Clarity": random.randint(8, 20) if brand else random.randint(5, 12),
        "Trust & Evidence": random.randint(10, 17),
        "Technical Accessibility": random.randint(14, 20)
    }
    
    total = sum(scores.values())
    
    # Classificazione
    if total < 40: label, color = "Debole", "red"
    elif total < 60: label, color = "Sufficiente ma fragile", "orange"
    elif total < 75: label, color = "Buona base, migliorabile", "blue"
    elif total < 90: label, color = "Forte", "green"
    else: label, color = "Eccellente per AI visibility", "#1D8348"
    
    return scores, total, label, color

# --- HEADER ---
st.title("🔍 GEO Score Tool")
st.subheader("Analizza quanto una pagina è pronta per la visibilità nei motori AI e scopri come migliorarla.")
st.markdown("---")

# --- FORM DI INPUT ---
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False

with st.container():
    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        st.markdown("### 📋 Dati Analisi")
        with st.form("audit_form"):
            url = st.text_input("URL della pagina da analizzare", placeholder="https://esempio.it/pagina")
            p_type = st.selectbox("Tipo di pagina", ["Homepage", "Pagina servizio", "Categoria", "Scheda prodotto", "Articolo blog", "Landing page"])
            keyword = st.text_input("Keyword principale", placeholder="es. consulenza marketing")
            brand = st.text_input("Brand", placeholder="es. Nome Agenzia")
            geo_area = st.text_input("Area geografica (facoltativa)")
            
            submit = st.form_submit_button("ANALIZZA PAGINA")
            if submit:
                if url:
                    st.session_state.analyzed = True
                    st.session_state.results = calculate_geo_logic(url, p_type, keyword, brand)
                else:
                    st.error("Inserisci un URL per procedere.")

# --- AREA RISULTATI ---
if st.session_state.analyzed:
    scores, total, label, color = st.session_state.results
    
    # SEZIONE 1: SINTESI
    st.markdown(f"## SEZIONE 1 — Sintesi")
    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown(f"""
            <div style="text-align: center; background: white; padding: 30px; border-radius: 20px; border: 2px solid {color};">
                <p style="margin-bottom: 0; color: #666;">GEO SCORE TOTALE</p>
                <div class="score-big" style="color: {color};">{total}/100</div>
                <div class="status-badge" style="background: {color}22; color: {color};">{label}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown("### Executive Summary")
        st.write(f"L'analisi della pagina per la keyword **{keyword}** mostra una preparazione **{label.lower()}**. "
                 f"Mentre la struttura tecnica è valida, segnali entitari legati al brand **{brand}** possono essere potenziati "
                 "per migliorare la citabilità nei motori generativi come Perplexity e ChatGPT.")
        st.metric("AI Citation Readiness", "ALTA" if total > 70 else "MEDIA")

    # SEZIONE 2: BREAKDOWN SCORE
    st.markdown("---")
    st.markdown("## SEZIONE 2 — Breakdown Score")
    cols = st.columns(5)
    for i, (name, val) in enumerate(scores.items()):
        with cols[i]:
            st.write(f"**{name}**")
            st.progress(val/20)
            st.write(f"{val}/20")

    # SEZIONE 3 & 4: PROBLEMI E AZIONI
    col_p, col_z = st.columns(2)
    
    with col_p:
        st.markdown("### ⚠️ Problemi Prioritari")
        problemi = [
            {"P": "Intro troppo generica", "C": "Content", "I": "Alto", "S": "Basso"},
            {"P": "Brand expertise poco esplicita", "C": "Entity", "I": "Alto", "S": "Medio"},
            {"P": "FAQ assenti", "C": "Structure", "I": "Medio", "S": "Basso"}
        ]
        for prob in problemi:
            with st.expander(f"{prob['P']} - Impatto: {prob['I']}"):
                st.write(f"**Categoria:** {prob['C']} | **Sforzo:** {prob['S']}")
                st.write("La pagina non definisce subito l'entità principale, rendendo difficile il retrieval per l'AI.")

    with col_z:
        st.markdown("### ✅ Azioni Consigliate")
        st.info("1. Aggiungi un blocco 'In sintesi' dopo l'H1.")
        st.info("2. Inserisci dati strutturati LocalBusiness/Organization.")
        st.info("3. Espandi la sezione Trust con casi studio reali.")

    # SEZIONE 6: SUGGERIMENTI GENERATIVI
    st.markdown("---")
    st.markdown("## SEZIONE 6 — Suggerimenti Generativi")
    t1, t2, t3 = st.tabs(["✍️ Intro & H2", "❓ FAQ suggerite", "🛠 Schema Markup"])
    
    with t1:
        st.code(f"Benvenuti su {brand}. Siamo specialisti in {keyword}...", language="text")
        st.button("Copia Intro")
    
    with t2:
        st.write(f"1. Cos'è {keyword}?")
        st.write(f"2. Perché scegliere {brand} per {geo_area}?")
        st.button("Copia FAQ")

    with t3:
        st.code(f'{{ "@context": "https://schema.org", "@type": "Organization", "name": "{brand}" }}', language="json")

    # FOOTER & CALL TO ACTION
    st.markdown("---")
    st.button("🔄 Nuova analisi", on_click=lambda: st.session_state.clear())
    st.success("Analisi completata con successo. Esporta il report in PDF per il tuo cliente.")
    
    st.markdown("""
        <div style="background: #007bff; color: white; padding: 20px; border-radius: 10px; text-align: center;">
            <h3>Vuoi trasformare questo report in un piano operativo?</h3>
            <p>Contattaci per una consulenza GEO dedicata.</p>
        </div>
    """, unsafe_allow_html=True)