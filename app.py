import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import anthropic

# ─────────────────────────────────────────
#  CONFIGURAZIONE PAGINA
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Alligator · GEO-Scanner Pro",
    page_icon="🐊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────
#  CSS / STILE
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600&display=swap');

/* ── Base ── */
:root {
    --green:       #00c853;
    --green-dim:   #00c85322;
    --dark:        #0d0d0d;
    --dark2:       #161616;
    --card:        #1c1c1c;
    --border:      #2a2a2a;
    --text:        #e8e8e8;
    --muted:       #888;
    --radius:      14px;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--dark) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}

/* hide streamlit chrome */
[data-testid="stHeader"],
[data-testid="stToolbar"],
footer { display: none !important; }

/* ── HERO ── */
.hero {
    background: linear-gradient(135deg, #0d0d0d 0%, #0a1f10 50%, #0d0d0d 100%);
    border-bottom: 1px solid var(--border);
    padding: 3.5rem 2rem 2.8rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 60% 60% at 50% 0%, rgba(0,200,83,.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-tag {
    display: inline-block;
    font-family: 'DM Sans', sans-serif;
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: var(--green);
    border: 1px solid var(--green);
    border-radius: 999px;
    padding: .25rem .85rem;
    margin-bottom: 1.1rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 6vw, 4rem);
    font-weight: 800;
    color: #fff;
    letter-spacing: -.02em;
    line-height: 1.05;
    margin: 0 0 .4rem;
}
.hero h1 span { color: var(--green); }
.hero p {
    color: var(--muted);
    font-size: 1rem;
    margin: 0;
}

/* ── CARDS ── */
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: .8rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: var(--green);
    margin-bottom: 1rem;
}

/* ── SCORE BADGE ── */
.score-wrap {
    text-align: center;
    padding: .6rem 0 1rem;
}
.score-number {
    font-family: 'Syne', sans-serif;
    font-size: 3.8rem;
    font-weight: 800;
    line-height: 1;
    color: #fff;
}
.score-label {
    display: inline-block;
    margin-top: .5rem;
    font-size: .78rem;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
    padding: .28rem .9rem;
    border-radius: 999px;
}
.score-critical  { background: #ff1744; color: #fff; }
.score-warning   { background: #ff9100; color: #000; }
.score-good      { background: #00e676; color: #000; }
.score-excellent { background: var(--green); color: #000; }

/* ── RESULT BOX ── */
.result-card {
    background: #111;
    border: 1px solid var(--border);
    border-left: 4px solid var(--green);
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem;
    white-space: pre-wrap;
    font-family: 'DM Sans', sans-serif;
    font-size: .9rem;
    line-height: 1.7;
    color: var(--text);
    margin-bottom: 1rem;
}

/* ── INPUTS ── */
[data-testid="stTextInput"] input {
    background: #111 !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: .6rem 1rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--green) !important;
    box-shadow: 0 0 0 2px var(--green-dim) !important;
}
label { color: var(--muted) !important; font-size: .82rem !important; font-weight: 500 !important; }

/* ── BUTTON ── */
[data-testid="stButton"] button {
    background: var(--green) !important;
    color: #000 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: .95rem !important;
    letter-spacing: .04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: .7rem 2.4rem !important;
    transition: opacity .2s, transform .15s !important;
}
[data-testid="stButton"] button:hover {
    opacity: .88 !important;
    transform: translateY(-1px) !important;
}

/* ── DIVIDER ── */
hr { border-color: var(--border) !important; }

/* ── SUCCESS / ERROR ── */
[data-testid="stAlert"] {
    background: var(--card) !important;
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
}

/* ── SPINNER TEXT ── */
[data-testid="stSpinner"] p { color: var(--green) !important; }

/* ── CODE BLOCK ── */
pre, code {
    background: #0a0a0a !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: #a8ff78 !important;
    font-size: .8rem !important;
}

/* Plotly transparent bg */
.js-plotly-plot .plotly, .js-plotly-plot .plotly .main-svg {
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  HELPER: Recupera secrets in modo sicuro
# ─────────────────────────────────────────
def get_secret(key: str) -> str | None:
    try:
        return st.secrets[key]
    except Exception:
        return None


# ─────────────────────────────────────────
#  ANALISI CON CLAUDE
# ─────────────────────────────────────────
def genera_analisi(brand: str, url: str, keyword: str) -> str:
    api_key = get_secret("ANTHROPIC_API_KEY")
    if not api_key:
        return "⚠️ ANTHROPIC_API_KEY non trovata nei Secrets. Aggiungila in Settings → Secrets."

    try:
        client = anthropic.Anthropic(api_key=api_key)
        prompt = f"""Sei il Senior GEO Expert di Alligator.it.
Analizza il brand **{brand}** (sito: {url}) per la keyword '{keyword}'.

RISPONDI IN ITALIANO CON QUESTI 3 BLOCCHI BEN SEPARATI:

## 1. DIAGNOSI TECNICA
Spiega in 3-5 punti perché le AI generative non citano questo sito.
Sii specifico e usa un tono consulenziale.

## 2. SCHEMA MARKUP JSON-LD
Genera il codice JSON-LD pronto da copiare (solo il tag <script type="application/ld+json">...</script>).
Commenta ogni campo importante.

## 3. TESTO OTTIMIZZATO PER LA HOME
Un paragrafo di 80-100 parole da inserire nella Home page.
Scrivi in modo naturale ma ottimizzato per essere citato dalle AI.
"""
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1800,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
    except anthropic.AuthenticationError:
        return "⚠️ API Key non valida. Verifica che ANTHROPIC_API_KEY sia corretta."
    except anthropic.RateLimitError:
        return "⚠️ Limite di utilizzo API raggiunto. Riprova tra qualche secondo."
    except Exception as e:
        return f"⚠️ Errore imprevisto durante l'analisi: {str(e)}"


# ─────────────────────────────────────────
#  INVIO MAIL
# ─────────────────────────────────────────
def invia_report_mail(brand: str, url: str, keyword: str, analisi: str,
                      email_cliente: str = "") -> tuple[bool, str]:
    """
    Invia il report a nicofioretti7@gmail.com.
    Ritorna (True, "") in caso di successo, (False, messaggio_errore) altrimenti.
    """
    email_password = get_secret("EMAIL_PASSWORD")
    if not email_password:
        return False, "EMAIL_PASSWORD non trovata nei Secrets."

    account   = "nicofioretti7@gmail.com"   # account Gmail che invia
    destinatario = "nicofioretti7@gmail.com" # dove vuoi ricevere i lead

    try:
        msg = MIMEMultipart()
        msg["From"]    = account
        msg["To"]      = destinatario
        msg["Subject"] = f"🐊 Nuovo Lead GEO: {brand}"

        corpo = (
            f"Nuova analisi GEO completata\n\n"
            f"Brand:   {brand}\n"
            f"URL:     {url}\n"
            f"Keyword: {keyword}\n"
            + (f"Email cliente: {email_cliente}\n" if email_cliente else "")
            + f"{'─'*40}\n\n"
            f"{analisi}"
        )
        msg.attach(MIMEText(corpo, "plain", "utf-8"))

        with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(account, email_password)
            server.sendmail(account, destinatario, msg.as_string())

        return True, ""

    except smtplib.SMTPAuthenticationError:
        return False, "Credenziali Gmail non valide. Usa una App Password (non la password normale)."
    except smtplib.SMTPException as e:
        return False, f"Errore SMTP: {e}"
    except Exception as e:
        return False, f"Errore generico: {e}"


# ─────────────────────────────────────────
#  CALCOLO GEO SCORE
# ─────────────────────────────────────────
def calcola_geo_score(scores: list[int]) -> tuple[int, str, str]:
    media = round(sum(scores) / len(scores))
    if media < 45:
        return media, "Critico", "score-critical"
    elif media < 60:
        return media, "Ottimizzabile", "score-warning"
    elif media < 80:
        return media, "Buono", "score-good"
    else:
        return media, "Eccellente", "score-excellent"


# ─────────────────────────────────────────
#  GRAFICO RADAR
# ─────────────────────────────────────────
def crea_radar(scores: list[int], brand: str) -> go.Figure:
    labels = ["Clarity", "Structure", "Entity", "Trust", "Tech"]
    # chiudi il poligono
    r = scores + [scores[0]]
    theta = labels + [labels[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=r,
        theta=theta,
        fill="toself",
        fillcolor="rgba(0,200,83,0.18)",
        line=dict(color="#00c853", width=2.5),
        marker=dict(color="#00c853", size=6),
        name=brand,
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color="#555", size=10),
                gridcolor="#2a2a2a",
                linecolor="#2a2a2a",
            ),
            angularaxis=dict(
                tickfont=dict(color="#e8e8e8", size=12, family="DM Sans"),
                gridcolor="#2a2a2a",
                linecolor="#2a2a2a",
            ),
        ),
        showlegend=False,
        margin=dict(t=30, b=30, l=40, r=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#e8e8e8"),
    )
    return fig


# ─────────────────────────────────────────
#  SPLIT ANALISI PER SEZIONI
# ─────────────────────────────────────────
def split_sezioni(testo: str) -> dict:
    """Suddivide la risposta di Claude nelle 3 sezioni."""
    sezioni = {"diagnosi": "", "jsonld": "", "testo": ""}

    blocchi = testo.split("##")
    for blocco in blocchi:
        b = blocco.strip()
        if b.lower().startswith("1.") or b.lower().startswith("1 ") or "diagnosi" in b.lower()[:30]:
            sezioni["diagnosi"] = b
        elif b.lower().startswith("2.") or b.lower().startswith("2 ") or "schema" in b.lower()[:30] or "json" in b.lower()[:30]:
            sezioni["jsonld"] = b
        elif b.lower().startswith("3.") or b.lower().startswith("3 ") or "testo" in b.lower()[:30]:
            sezioni["testo"] = b

    # fallback: mostra tutto in diagnosi se split fallisce
    if not any(sezioni.values()):
        sezioni["diagnosi"] = testo

    return sezioni


# ─────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-tag">GEO · Generative Engine Optimization</div>
    <h1>🐊 ALLIGATOR<br><span>GEO-Scanner Pro</span></h1>
    <p>Analisi AI-ready per far citare il tuo brand da ChatGPT, Gemini e Perplexity.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  FORM
# ─────────────────────────────────────────
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>⚙️ Configura l'Audit</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        u = st.text_input("URL Sito", placeholder="https://tuosito.it")
        b = st.text_input("Nome Brand", placeholder="Alligator")
    with col2:
        k = st.text_input("Keyword Target", placeholder="agenzia SEO Milano")
        m = st.text_input("La tua Email (opzionale)", placeholder="tu@email.com")

    st.markdown("</div>", unsafe_allow_html=True)

_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    avvia = st.button("🐊 ANALIZZA ORA", use_container_width=True)

# ─────────────────────────────────────────
#  ELABORAZIONE
# ─────────────────────────────────────────
if avvia:
    if not (u and b and k):
        st.error("Inserisci URL, Brand e Keyword per avviare l'analisi.")
    else:
        with st.spinner("Alligator sta elaborando il tuo report con Claude AI…"):

            # 1. Analisi AI
            risultato_ai = genera_analisi(b, u, k)

            # 2. Scores simulati per radar
            scores = [random.randint(38, 88) for _ in range(5)]
            geo_score, geo_label, geo_css = calcola_geo_score(scores)

            # 3. Invio mail
            mail_ok, mail_err = invia_report_mail(b, u, k, risultato_ai, m)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")

        # ── Layout risultati ──
        left, right = st.columns([1, 1.4], gap="large")

        with left:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-title'>📡 GEO Radar Score</div>", unsafe_allow_html=True)

            fig = crea_radar(scores, b)
            st.plotly_chart(fig, use_container_width=True)

            # Score complessivo
            st.markdown(f"""
            <div class='score-wrap'>
                <div class='score-number'>{geo_score}<span style='font-size:1.6rem;color:var(--muted)'>%</span></div>
                <span class='score-label {geo_css}'>{geo_label}</span>
            </div>
            """, unsafe_allow_html=True)

            # Mini breakdown
            labels = ["Clarity", "Structure", "Entity", "Trust", "Tech"]
            for label, s in zip(labels, scores):
                bar_w = s
                color = "#00c853" if s >= 70 else "#ff9100" if s >= 50 else "#ff1744"
                st.markdown(f"""
                <div style='margin-bottom:.5rem'>
                    <div style='display:flex;justify-content:space-between;margin-bottom:.2rem'>
                        <span style='font-size:.78rem;color:var(--muted)'>{label}</span>
                        <span style='font-size:.78rem;font-weight:600;color:#fff'>{s}</span>
                    </div>
                    <div style='background:#2a2a2a;border-radius:999px;height:5px'>
                        <div style='width:{bar_w}%;height:5px;border-radius:999px;background:{color};transition:width .6s'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with right:
            sezioni = split_sezioni(risultato_ai)

            # ── Diagnosi Tecnica ──
            if sezioni["diagnosi"]:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("<div class='card-title'>🔍 Diagnosi Tecnica</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='result-card'>{sezioni['diagnosi']}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # ── JSON-LD ──
            if sezioni["jsonld"]:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("<div class='card-title'>📋 Schema Markup JSON-LD — Copia & Incolla</div>", unsafe_allow_html=True)
                st.code(sezioni["jsonld"], language="json")
                st.markdown("</div>", unsafe_allow_html=True)

            # ── Testo ottimizzato ──
            if sezioni["testo"]:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("<div class='card-title'>✍️ Testo Ottimizzato per la Home</div>", unsafe_allow_html=True)
                st.code(sezioni["testo"], language="markdown")
                st.markdown("</div>", unsafe_allow_html=True)

            # ── Fallback: tutto in un blocco ──
            if not sezioni["jsonld"] and not sezioni["testo"] and not sezioni["diagnosi"]:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("<div class='card-title'>📋 Report Completo</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='result-card'>{risultato_ai}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        # ── Notifica finale ──
        st.markdown("<br>", unsafe_allow_html=True)
        if mail_ok:
            st.success("✅ Analisi completata. Report inviato con successo all'agenzia.")
        else:
            st.success("✅ Analisi completata.")
            if mail_err:
                st.warning(f"⚠️ Invio mail fallito: {mail_err}")
