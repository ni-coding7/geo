import streamlit as st
import plotly.graph_objects as go
import smtplib
import random
import io
import anthropic

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from docx import Document as DocxDocument
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# ─────────────────────────────────────────
st.set_page_config(
    page_title="Alligator · GEO-Scanner Pro",
    page_icon="🐊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;900&family=Open+Sans:wght@400;500;600&display=swap');

:root {
    --green:      #1a7a3c;
    --green-light:#22a04f;
    --green-pale: #eaf5ee;
    --green-mid:  #155f2f;
    --white:      #ffffff;
    --offwhite:   #f5f9f6;
    --text:       #1a2e22;
    --muted:      #557060;
    --border:     #c5dece;
    --radius:     12px;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--offwhite) !important;
    color: var(--text) !important;
    font-family: 'Open Sans', sans-serif;
}

[data-testid="stHeader"], [data-testid="stToolbar"], footer { display:none!important; }

.hero {
    background: linear-gradient(135deg, var(--green) 0%, var(--green-mid) 100%);
    padding: 4rem 2rem 3.2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    border-radius: 0 0 32px 32px;
    margin-bottom: 2.5rem;
}
.hero-eyebrow {
    display: inline-block;
    background: rgba(255,255,255,.15);
    border: 1px solid rgba(255,255,255,.3);
    color: #fff;
    font-family:'Montserrat',sans-serif;
    font-size:.7rem;
    font-weight:700;
    letter-spacing:.2em;
    text-transform:uppercase;
    border-radius:999px;
    padding:.3rem 1rem;
    margin-bottom:1.2rem;
}
.hero h1 {
    font-family:'Montserrat',sans-serif;
    font-size: clamp(2rem,5vw,3.4rem);
    font-weight:900;
    color:#fff;
    line-height:1.1;
    margin:0 0 .6rem;
    letter-spacing:-.02em;
}
.hero h1 em { font-style:normal; color: #a8f0c0; }
.hero p { color:rgba(255,255,255,.82); font-size:1.02rem; margin:0; }
.partner-badge {
    display:inline-flex;
    align-items:center;
    gap:.5rem;
    background:rgba(255,255,255,.1);
    border:1px solid rgba(255,255,255,.25);
    border-radius:8px;
    padding:.4rem .9rem;
    margin-top:1.2rem;
    color:#fff;
    font-size:.75rem;
    font-weight:600;
    letter-spacing:.05em;
}

.card {
    background:var(--white);
    border:1px solid var(--border);
    border-radius:var(--radius);
    padding:1.6rem 1.8rem;
    margin-bottom:1.2rem;
    box-shadow:0 2px 12px rgba(26,122,60,.07);
}
.card-title {
    font-family:'Montserrat',sans-serif;
    font-weight:700;
    font-size:.72rem;
    letter-spacing:.15em;
    text-transform:uppercase;
    color:var(--green);
    margin-bottom:1rem;
    padding-bottom:.5rem;
    border-bottom:2px solid var(--green-pale);
}

.score-wrap { text-align:center; padding:.4rem 0 .8rem; }
.score-number {
    font-family:'Montserrat',sans-serif;
    font-size:3.6rem;
    font-weight:900;
    color:var(--green);
    line-height:1;
}
.score-sub { font-size:.85rem; color:var(--muted); margin-top:.3rem; }
.score-pill {
    display:inline-block;
    margin-top:.5rem;
    font-size:.72rem;
    font-weight:700;
    letter-spacing:.1em;
    text-transform:uppercase;
    padding:.3rem 1rem;
    border-radius:999px;
}
.pill-critical  { background:#ffebee; color:#c62828; border:1px solid #ef9a9a; }
.pill-warning   { background:#fff8e1; color:#e65100; border:1px solid #ffcc02; }
.pill-good      { background:#e8f5e9; color:#2e7d32; border:1px solid #a5d6a7; }
.pill-excellent { background:var(--green); color:#fff; }

.result-card {
    background:var(--offwhite);
    border-left:4px solid var(--green);
    border-radius:0 var(--radius) var(--radius) 0;
    padding:1.2rem 1.4rem;
    white-space:pre-wrap;
    font-size:.9rem;
    line-height:1.75;
    color:var(--text);
}
.info-box {
    background:var(--green-pale);
    border:1px solid var(--border);
    border-radius:var(--radius);
    padding:1rem 1.4rem;
    font-size:.88rem;
    color:var(--green-mid);
    display:flex;
    gap:.7rem;
    align-items:flex-start;
}

[data-testid="stTextInput"] input {
    background:#fff !important;
    border:1.5px solid var(--border) !important;
    border-radius:9px !important;
    color:var(--text) !important;
    font-family:'Open Sans',sans-serif !important;
}
[data-testid="stTextInput"] input:focus {
    border-color:var(--green) !important;
    box-shadow:0 0 0 3px rgba(26,122,60,.12) !important;
}
label { color:var(--muted) !important; font-size:.8rem !important; font-weight:600 !important; }

[data-testid="stButton"] button {
    background:var(--green) !important;
    color:#fff !important;
    font-family:'Montserrat',sans-serif !important;
    font-weight:700 !important;
    font-size:.92rem !important;
    letter-spacing:.05em !important;
    border:none !important;
    border-radius:10px !important;
    padding:.72rem 2.4rem !important;
    transition:background .2s,transform .15s !important;
}
[data-testid="stButton"] button:hover {
    background:var(--green-light) !important;
    transform:translateY(-1px) !important;
}
[data-testid="stAlert"] { border-radius:var(--radius) !important; }
[data-testid="stSpinner"] p { color:var(--green) !important; }
.js-plotly-plot .plotly,.js-plotly-plot .plotly .main-svg { background:transparent!important; }
</style>
""", unsafe_allow_html=True)


# ─── HELPERS ───────────────────────────────────────────────────────
def get_secret(key):
    try:
        return st.secrets[key]
    except Exception:
        return None


# ─── CLAUDE ────────────────────────────────────────────────────────
def genera_analisi(brand, url, keyword):
    api_key = get_secret("ANTHROPIC_API_KEY")
    if not api_key:
        return "ERRORE: ANTHROPIC_API_KEY non configurata nei Secrets."
    try:
        client = anthropic.Anthropic(api_key=api_key)
        prompt = f"""Sei il Senior GEO Expert di Alligator.it.
Analizza il brand **{brand}** (sito: {url}) per la keyword '{keyword}'.

RISPONDI IN ITALIANO con questi 3 blocchi separati ESATTAMENTE con questi titoli:

## DIAGNOSI
3-5 punti chiari su perché le AI generative (ChatGPT, Gemini, Perplexity) non citano questo sito.
Usa un tono consulenziale professionale. NON menzionare schemi markup o codice tecnico in questa sezione.

## JSON_LD
Genera il codice Schema.org JSON-LD completo pronto da incollare, incluso il tag <script type="application/ld+json">. Commenta ogni campo.

## TESTO_HOME
Un paragrafo di 80-100 parole ottimizzato GEO da inserire nella Home page.
"""
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
    except anthropic.AuthenticationError:
        return "ERRORE: API Key Anthropic non valida."
    except anthropic.RateLimitError:
        return "ERRORE: Limite API raggiunto. Riprova tra qualche secondo."
    except Exception as e:
        return f"ERRORE: {e}"


def split_sezioni(testo):
    sezioni = {"diagnosi": "", "jsonld": "", "testo": ""}
    blocchi = testo.split("##")
    for b in blocchi:
        b = b.strip()
        low = b.lower()
        if low.startswith("diagnosi"):
            sezioni["diagnosi"] = b[len("diagnosi"):].strip()
        elif low.startswith("json_ld") or low.startswith("json-ld") or low.startswith("jsonld"):
            parts = b.split(None, 1)
            sezioni["jsonld"] = parts[1].strip() if len(parts) > 1 else b
        elif low.startswith("testo"):
            parts = b.split(None, 1)
            sezioni["testo"] = parts[1].strip() if len(parts) > 1 else b
    if not any(sezioni.values()):
        sezioni["diagnosi"] = testo
    return sezioni


# ─── CREA DOCX ─────────────────────────────────────────────────────
def crea_docx(brand, url, keyword, diagnosi, jsonld, testo, scores, geo_score, geo_label):
    doc = DocxDocument()

    # stile base
    doc.styles["Normal"].font.name = "Arial"
    doc.styles["Normal"].font.size = Pt(11)

    def colored_heading(text, level, rgb):
        p = doc.add_heading(text, level=level)
        for run in p.runs:
            run.font.color.rgb = RGBColor(*rgb)
        return p

    # Intestazione
    doc.add_paragraph()
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = title.add_run("🐊  ALLIGATOR · GEO-Scanner Pro")
    r.font.size = Pt(20); r.font.bold = True
    r.font.color.rgb = RGBColor(0x1a, 0x7a, 0x3c)

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle.add_run(f"Report Tecnico Riservato — {brand}").font.size = Pt(12)

    doc.add_paragraph()
    doc.add_paragraph(f"Brand:    {brand}")
    doc.add_paragraph(f"URL:      {url}")
    doc.add_paragraph(f"Keyword:  {keyword}")
    doc.add_paragraph()

    # Score
    colored_heading("GEO Score Complessivo", 1, (0x1a, 0x7a, 0x3c))
    sp = doc.add_paragraph(f"Score: {geo_score}/100  —  Stato: {geo_label}")
    sp.runs[0].font.bold = True; sp.runs[0].font.size = Pt(12)
    labels = ["Clarity", "Structure", "Entity", "Trust", "Tech"]
    for lbl, s in zip(labels, scores):
        doc.add_paragraph(f"  • {lbl}: {s}/100")
    doc.add_paragraph()

    # Diagnosi
    colored_heading("Diagnosi Tecnica", 1, (0x1a, 0x7a, 0x3c))
    doc.add_paragraph(diagnosi or "Non disponibile.")
    doc.add_paragraph()

    # JSON-LD
    colored_heading("Schema Markup JSON-LD", 1, (0x1a, 0x7a, 0x3c))
    doc.add_paragraph("Inserire questo codice nell'<head> di ogni pagina rilevante:")
    cp = doc.add_paragraph(jsonld or "Non disponibile.")
    if cp.runs:
        cp.runs[0].font.name = "Courier New"
        cp.runs[0].font.size = Pt(9)
    doc.add_paragraph()

    # Testo Home
    colored_heading("Testo Ottimizzato per la Home Page", 1, (0x1a, 0x7a, 0x3c))
    doc.add_paragraph(testo or "Non disponibile.")
    doc.add_paragraph()

    # Nota interna
    colored_heading("Note Interne Agenzia", 2, (0x15, 0x5f, 0x2f))
    doc.add_paragraph(
        "Documento riservato ad uso interno Alligator. "
        "Applicare le implementazioni tecniche prima di condividere risultati con il cliente."
    )

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf.read()


# ─── MAIL + ALLEGATO ───────────────────────────────────────────────
def invia_report_mail(brand, url, keyword, email_cliente,
                      diagnosi, jsonld, testo, scores, geo_score, geo_label):
    email_password = get_secret("EMAIL_PASSWORD")
    if not email_password:
        return False, "EMAIL_PASSWORD non trovata nei Secrets."

    account = destinatario = "nicofioretti7@gmail.com"

    try:
        docx_bytes = crea_docx(brand, url, keyword, diagnosi,
                                jsonld, testo, scores, geo_score, geo_label)

        msg = MIMEMultipart()
        msg["From"] = account
        msg["To"] = destinatario
        msg["Subject"] = f"🐊 Nuovo Lead GEO: {brand}"

        corpo = (
            f"Nuovo audit GEO completato.\n\n"
            f"Brand:   {brand}\n"
            f"URL:     {url}\n"
            f"Keyword: {keyword}\n"
            + (f"Email cliente: {email_cliente}\n" if email_cliente else "")
            + f"\nGEO Score: {geo_score}/100 — {geo_label}\n\n"
            "Il report tecnico completo (JSON-LD + testo Home) è in allegato .docx\n"
            "— Alligator GEO-Scanner Pro"
        )
        msg.attach(MIMEText(corpo, "plain", "utf-8"))

        part = MIMEBase(
            "application",
            "vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        part.set_payload(docx_bytes)
        encoders.encode_base64(part)
        filename = f"GEO_Report_{brand.replace(' ', '_')}.docx"
        part.add_header("Content-Disposition", "attachment", filename=filename)
        msg.attach(part)

        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
            server.ehlo(); server.starttls(); server.ehlo()
            server.login(account, email_password)
            server.sendmail(account, destinatario, msg.as_string())

        return True, ""

    except smtplib.SMTPAuthenticationError:
        return False, "Credenziali Gmail non valide. Usa una App Password."
    except smtplib.SMTPException as e:
        return False, f"Errore SMTP: {e}"
    except Exception as e:
        return False, f"Errore: {e}"


# ─── RADAR ─────────────────────────────────────────────────────────
def crea_radar(scores, brand):
    labels = ["Clarity", "Structure", "Entity", "Trust", "Tech"]
    r = scores + [scores[0]]; theta = labels + [labels[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=r, theta=theta, fill="toself",
        fillcolor="rgba(26,122,60,0.15)",
        line=dict(color="#1a7a3c", width=2.5),
        marker=dict(color="#1a7a3c", size=7),
        name=brand,
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100],
                            tickfont=dict(color="#888", size=9),
                            gridcolor="#c5dece", linecolor="#c5dece"),
            angularaxis=dict(tickfont=dict(color="#1a2e22", size=12, family="Open Sans"),
                             gridcolor="#c5dece", linecolor="#c5dece"),
        ),
        showlegend=False,
        margin=dict(t=30, b=30, l=40, r=40),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def calcola_geo_score(scores):
    media = round(sum(scores) / len(scores))
    if media < 45:   return media, "Critico",      "pill-critical"
    elif media < 60: return media, "Ottimizzabile", "pill-warning"
    elif media < 80: return media, "Buono",         "pill-good"
    else:            return media, "Eccellente",    "pill-excellent"


# ─── HERO ──────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">GEO · Generative Engine Optimization</div>
    <h1>🐊 ALLIGATOR<br><em>GEO-Scanner Pro</em></h1>
    <p>Scopri perché ChatGPT, Gemini e Perplexity non citano il tuo brand<br>
       e ricevi il piano d'azione dalla tua agenzia.</p>
    <div class="partner-badge">⭐ Google Premier Partner 2025</div>
</div>
""", unsafe_allow_html=True)


# ─── FORM ──────────────────────────────────────────────────────────
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div class='card-title'>⚙️ Configura il tuo Audit GEO</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")
with col1:
    u = st.text_input("URL Sito Web", placeholder="https://tuosito.it")
    b = st.text_input("Nome Brand", placeholder="Es. Alligator")
with col2:
    k = st.text_input("Keyword Principale", placeholder="Es. agenzia SEO Milano")
    m = st.text_input("La tua Email (opzionale)", placeholder="tu@email.it")

st.markdown("</div>", unsafe_allow_html=True)

_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    avvia = st.button("🐊 AVVIA AUDIT GEO", use_container_width=True)


# ─── ELABORAZIONE ──────────────────────────────────────────────────
if avvia:
    if not (u and b and k):
        st.error("Inserisci URL, Brand e Keyword per avviare l'analisi.")
    else:
        with st.spinner("Alligator sta analizzando il tuo brand con Claude AI…"):
            risultato_ai = genera_analisi(b, u, k)
            sezioni = split_sezioni(risultato_ai)

            scores = [random.randint(35, 85) for _ in range(5)]
            geo_score, geo_label, geo_css = calcola_geo_score(scores)

            # Mail con docx allegato — tutto il tecnico rimane privato
            mail_ok, mail_err = invia_report_mail(
                b, u, k, m,
                sezioni["diagnosi"], sezioni["jsonld"], sezioni["testo"],
                scores, geo_score, geo_label,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        left, right = st.columns([1, 1.45], gap="large")

        with left:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-title'>📡 Radar GEO Score</div>", unsafe_allow_html=True)
            st.plotly_chart(crea_radar(scores, b), use_container_width=True)

            st.markdown(f"""
            <div class='score-wrap'>
                <div class='score-number'>{geo_score}<span style='font-size:1.4rem;color:var(--muted)'>/100</span></div>
                <div class='score-sub'>GEO Score Complessivo</div>
                <span class='score-pill {geo_css}'>{geo_label}</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            labels_r = ["Clarity", "Structure", "Entity", "Trust", "Tech"]
            for lbl, s in zip(labels_r, scores):
                color = "#1a7a3c" if s >= 70 else "#e65100" if s >= 50 else "#c62828"
                st.markdown(f"""
                <div style='margin-bottom:.55rem'>
                    <div style='display:flex;justify-content:space-between;margin-bottom:.2rem'>
                        <span style='font-size:.78rem;color:var(--muted);font-weight:600'>{lbl}</span>
                        <span style='font-size:.78rem;font-weight:700;color:var(--text)'>{s}</span>
                    </div>
                    <div style='background:#e8f0ec;border-radius:999px;height:6px'>
                        <div style='width:{s}%;height:6px;border-radius:999px;background:{color}'></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with right:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("<div class='card-title'>🔍 Analisi GEO del tuo Brand</div>", unsafe_allow_html=True)

            diagnosi_display = sezioni["diagnosi"] if sezioni["diagnosi"] else risultato_ai
            st.markdown(f"<div class='result-card'>{diagnosi_display}</div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div class='info-box'>
                <span style='font-size:1.3rem'>📬</span>
                <div>
                    <strong>Prossimo passo</strong><br>
                    Il tuo piano d'azione personalizzato è pronto.
                    Un esperto Alligator ti contatterà per illustrarti le implementazioni
                    e i tempi di risultato attesi.
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if mail_ok:
            st.success("✅ Audit completato! Il report tecnico è stato inviato all'agenzia Alligator.")
        else:
            st.success("✅ Audit completato!")
            if mail_err:
                st.warning(f"⚠️ Invio report fallito: {mail_err}")
