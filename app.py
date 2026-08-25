
import streamlit as st

from questions import questions
from scoring import calculate_result
from outcomes import outcomes


# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Descubre tu trayectoria",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ============================================================
# ICONOS Y COLORES (perfil/interés solo para la pantalla de resultado)
# ============================================================

PROFILE_ICONS = {
    "Escalador": "🚀",
    "Aprendiz": "📚",
    "Equilibrado": "⚖️",
    "Especialista": "🎯",
    "Innovador": "💡"
}

INTEREST_ICONS = {
    "Tecnologia": "💻",
    "Finanzas": "💰",
    "Estrategia": "📈",
    "Negocio": "🤝",
    "Personas": "👥",
    "Juridico": "⚖️",
    "Sostenibilidad": "🌱"
}

PROFILE_COLORS = {
    "Escalador": "#E8703F",
    "Aprendiz": "#2CA9A0",
    "Equilibrado": "#D65C96",
    "Especialista": "#F2A93C",
    "Innovador": "#B5482E",
}

INTEREST_COLORS = {
    "Tecnologia": "#2CA9A0",
    "Finanzas": "#F2A93C",
    "Estrategia": "#004481",
    "Negocio": "#E8703F",
    "Personas": "#D65C96",
    "Juridico": "#12294A",
    "Sostenibilidad": "#1E8F72",
}

DEFAULT_ACCENT = "#004481"

# -----------------------------------------------------------
# Paleta puramente decorativa para las opciones del cuestionario.
# NO tiene relación con el perfil/interés real de cada respuesta:
# solo rota por posición, para no condicionar al usuario.
# -----------------------------------------------------------
DECORATIVE_PALETTE = [
    "#E8703F",  # naranja
    "#2CA9A0",  # teal
    "#D65C96",  # rosa
    "#F2A93C",  # ámbar
    "#004481",  # navy
]


def decorative_colors(question_id, num_options):
    """Devuelve una lista de colores decorativos para las opciones
    de una pregunta, rotando la paleta con un desplazamiento distinto
    por pregunta (para que no siempre empiece igual)."""
    offset = (question_id * 2) % len(DECORATIVE_PALETTE)
    return [
        DECORATIVE_PALETTE[(offset + i) % len(DECORATIVE_PALETTE)]
        for i in range(num_options)
    ]


# ============================================================
# ESTILOS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Montserrat:wght@300;400;500;600;700&display=swap');

:root{
    --color-primary:#004481;
    --color-primary-dark:#00305C;
    --color-accent:#2CA9A0;
    --color-accent-soft:#E3F6F3;
    --color-bg:#F5F8FA;
    --color-surface:#FFFFFF;
    --color-border:#E1E7ED;
    --color-text:#0B1F33;
    --color-text-muted:#5C6B7A;
}

html, body, [class*="css"]{
    font-family:'Montserrat', sans-serif;
    color:var(--color-text);
}

.stApp{
    background:var(--color-bg);
}

#MainMenu{ visibility:hidden; }
footer{ visibility:hidden; }
header{ visibility:hidden; }

.block-container{
    max-width:760px !important;
    margin:0 auto !important;
    padding-top:40px !important;
    padding-bottom:60px !important;
}

div[data-testid="stHorizontalBlock"]{
    display:flex !important;
    width:100% !important;
    gap:16px !important;
}

div[data-testid="stColumn"]{
    flex:1 1 0 !important;
    width:100% !important;
    min-width:0 !important;
}

h1, h2, h3{
    font-family:'Sora', sans-serif;
    color:var(--color-primary);
}

h1{
    text-align:center;
    font-weight:800;
    letter-spacing:-0.5px;
}

h2{ font-weight:700; }

p{
    font-size:17px;
    line-height:1.7;
    color:var(--color-text-muted);
}

.eyebrow{
    text-align:center;
    text-transform:uppercase;
    letter-spacing:2px;
    font-size:13px;
    font-weight:700;
    color:var(--color-accent);
    margin-bottom:8px;
}

.feature-row{
    display:flex;
    justify-content:center;
    gap:28px;
    margin-top:28px;
    margin-bottom:8px;
    flex-wrap:wrap;
}

.feature-item{
    text-align:center;
    font-size:14px;
    color:var(--color-text-muted);
    max-width:140px;
}

.feature-item .icon{
    font-size:26px;
    display:block;
    margin-bottom:6px;
}

.step-indicator{
    display:flex;
    justify-content:center;
    gap:8px;
    margin-bottom:6px;
    flex-wrap:wrap;
}

.step-dot{
    width:10px;
    height:10px;
    border-radius:50%;
    background:var(--color-border);
    transition:all .2s ease;
}

.step-dot.done{ background:var(--color-accent); }

.step-dot.current{
    background:var(--color-primary);
    transform:scale(1.35);
}

.step-caption{
    text-align:center;
    color:var(--color-text-muted);
    font-size:14px;
    font-weight:600;
    margin-bottom:24px;
}

/* -----------------------------------------------------------
   BOTONES (Comenzar / Anterior / Siguiente)
----------------------------------------------------------- */
div[data-testid="stElementContainer"]:has(> div.stButton){
    width:100% !important;
}

div.stButton{
    display:flex !important;
    justify-content:center !important;
    width:100% !important;
}

div.stButton button{
    width:100% !important;
    height:54px !important;
    border-radius:12px !important;
    border:none !important;
    background:var(--color-primary) !important;
    font-family:'Montserrat', sans-serif !important;
    font-size:16px !important;
    font-weight:600 !important;
    transition:all .2s ease !important;
    display:flex !important;
    align-items:center !important;
    justify-content:center !important;
    text-align:center !important;
}

div.stButton button * {
    color:white !important;
}

div.stButton button:hover{
    background:var(--color-primary-dark) !important;
    box-shadow:0 4px 14px rgba(0,68,129,.25) !important;
}

div[data-testid="stColumn"]:nth-of-type(1) div.stButton button{
    background:transparent !important;
    border:2px solid var(--color-border) !important;
    height:50px !important;
    box-shadow:none !important;
}

div[data-testid="stColumn"]:nth-of-type(1) div.stButton button *{
    color:var(--color-primary) !important;
}

div[data-testid="stColumn"]:nth-of-type(1) div.stButton button:hover{
    background:var(--color-bg) !important;
    border-color:var(--color-primary) !important;
}

/* -----------------------------------------------------------
   OPCIONES COMO BOTONES
----------------------------------------------------------- */
div[data-testid="stRadio"]{
    width:100% !important;
}

div[data-testid="stRadioGroup"]{
    width:100% !important;
    display:flex !important;
    flex-direction:column !important;
    gap:12px !important;
}

label[data-testid="stRadioOption"]{
    width:100% !important;
    box-sizing:border-box !important;
    min-height:56px !important;
    display:flex !important;
    align-items:center !important;
    border:1.5px solid var(--color-border) !important;
    border-left-width:6px !important;
    border-radius:14px !important;
    padding:16px 18px !important;
    background:var(--color-surface) !important;
    box-shadow:0 1px 3px rgba(11,31,51,0.05) !important;
    transition:all .18s ease !important;
    cursor:pointer !important;
}

label[data-testid="stRadioOption"] p{
    font-size:18px !important;
    color:var(--color-text) !important;
}

label[data-testid="stRadioOption"]:hover{
    background:var(--color-accent-soft) !important;
    box-shadow:0 4px 12px rgba(11,31,51,0.1) !important;
}

.tag-row{
    display:flex;
    justify-content:center;
    gap:10px;
    margin-top:14px;
    flex-wrap:wrap;
}

.tag-pill{
    padding:6px 16px;
    border-radius:999px;
    font-size:13px;
    font-weight:700;
    color:white;
}

.hero-result{
    border-radius:20px;
    padding:40px 32px;
    text-align:center;
    color:white;
    box-shadow:0 8px 24px rgba(0,68,129,.2);
}

.hero-icon{ font-size:42px; margin-bottom:10px; }

.hero-result h2{
    color:white;
    font-size:26px;
    margin-bottom:6px;
}

.hero-result p{
    color:rgba(255,255,255,.9);
    font-size:17px;
    max-width:520px;
    margin:0 auto;
}

.timeline{ margin-top:10px; }

.timeline-item{
    position:relative;
    display:flex;
    gap:18px;
    padding-bottom:28px;
}

.timeline-item:last-child{ padding-bottom:0; }

.timeline-node{
    flex-shrink:0;
    width:40px;
    height:40px;
    border-radius:50%;
    background:var(--color-primary);
    color:white;
    display:flex;
    align-items:center;
    justify-content:center;
    font-family:'Sora', sans-serif;
    font-weight:700;
    font-size:15px;
    position:relative;
    z-index:2;
    box-shadow:0 0 0 6px var(--color-bg);
}

.timeline-item:not(:last-child)::before{
    content:'';
    position:absolute;
    left:19px;
    top:40px;
    width:2px;
    height:calc(100% - 12px);
    background:var(--color-border);
    z-index:1;
}

.timeline-content{
    background:var(--color-surface);
    border:1px solid var(--color-border);
    border-radius:14px;
    padding:16px 20px;
    font-size:16px;
    color:var(--color-text);
    flex:1;
    box-shadow:0 1px 3px rgba(11,31,51,0.04);
}

/* -----------------------------------------------------------
   FORZAR TEMA CLARO
----------------------------------------------------------- */

html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], [data-testid="stMain"] {
    background-color: #F5F8FA !important;
    color: #0B1F33 !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #004481 !important;
}

.stMarkdown p,
.stMarkdown span,
.stMarkdown label {
    color: #0B1F33 !important;
}

p {
    color: #5C6B7A !important;
}

[data-baseweb="radio"],
[data-baseweb="radio"] label,
[data-baseweb="radio"] label p {
    color: #0B1F33 !important;
}

div.stButton button,
div.stButton button p {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# VARIABLES DE SESIÓN
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(questions)


# ============================================================
# PANTALLA DE BIENVENIDA
# ============================================================

if st.session_state.page == "welcome":

    total_questions = len(questions)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        "<div class='eyebrow'>Orientación profesional</div>",
        unsafe_allow_html=True
    )

    st.title("Descubre tu posible trayectoria profesional")

    st.markdown(
        f"""
        <div style="text-align:center; font-size:18px; color:var(--color-text-muted); max-width:560px; margin:0 auto;">
        Responde <b>{total_questions} preguntas</b> y descubre qué recorrido
        profesional podría encajar mejor contigo dentro de una gran empresa.
        </div>

        <div class="feature-row">
            <div class="feature-item">
                <span class="icon">📝</span>
                {total_questions} preguntas
            </div>
            <div class="feature-item">
                <span class="icon">⏱️</span>
                Sin límite de tiempo
            </div>
            <div class="feature-item">
                <span class="icon">🎯</span>
                Resultado personalizado
            </div>
        </div>

        <div style="text-align:center; font-size:15px; color:var(--color-text-muted); margin-top:24px;">
        No existen respuestas correctas o incorrectas.<br>
        Responde según lo que realmente te motive.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Comenzar"):
        st.session_state.page = "quiz"
        st.session_state.current_question = 0
        st.rerun()


# ============================================================
# CUESTIONARIO
# ============================================================

elif st.session_state.page == "quiz":

    total_questions = len(questions)
    current = st.session_state.current_question

    dots_html = "<div class='step-indicator'>"
    for i in range(total_questions):
        if i < current:
            dots_html += "<div class='step-dot done'></div>"
        elif i == current:
            dots_html += "<div class='step-dot current'></div>"
        else:
            dots_html += "<div class='step-dot'></div>"
    dots_html += "</div>"

    st.markdown(dots_html, unsafe_allow_html=True)

    st.markdown(
        f"<div class='step-caption'>Pregunta {current + 1} de {total_questions}</div>",
        unsafe_allow_html=True
    )

    question = questions[current]

    st.markdown(
        f"<h2 style='text-align:center;'>{question['question']}</h2>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # Estilo por pregunta:
    # - color decorativo por opción (sin relación con el scoring)
    # - dos columnas si hay muchas opciones cortas (>8)
    # -----------------------------

    num_options = len(question["options"])
    colors = decorative_colors(question["id"], num_options)

    dynamic_style = "<style>"

    for idx, color in enumerate(colors, start=1):
        dynamic_style += (
            f"div[data-testid='stRadioGroup'] > label[data-testid='stRadioOption']:nth-of-type({idx})"
            f"{{border-left-color:{color} !important;}}"
        )

    if num_options > 8:
        dynamic_style += """
        div[data-testid='stRadioGroup']{
            display:grid !important;
            grid-template-columns:1fr 1fr !important;
            gap:12px !important;
        }
        """

    dynamic_style += "</style>"

    st.markdown(dynamic_style, unsafe_allow_html=True)

    # -----------------------------
    # Opciones
    # -----------------------------

    options = [option["text"] for option in question["options"]]

    previous_answer = st.session_state.answers[current]

    answer = st.radio(
        label="",
        options=options,
        index=previous_answer if previous_answer is not None else None,
        key=f"question_{current}"
    )

    if answer is not None:
        st.session_state.answers[current] = options.index(answer)

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # Botones
    # Si no hay "Anterior" (primera pregunta), no creamos columnas:
    # un único botón a ancho completo, en vez de mitad de pantalla.
    # -----------------------------

    if current == 0:

        if current == total_questions - 1:
            if st.button("Ver mi trayectoria 🚀"):
                if st.session_state.answers[current] is None:
                    st.warning("Selecciona una respuesta antes de continuar.")
                else:
                    st.session_state.page = "result"
                    st.rerun()
        else:
            if st.button("Siguiente ➜"):
                if st.session_state.answers[current] is None:
                    st.warning("Selecciona una respuesta antes de continuar.")
                else:
                    st.session_state.current_question += 1
                    st.rerun()

    else:

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⬅ Anterior"):
                st.session_state.current_question -= 1
                st.rerun()

        with col2:
            if current == total_questions - 1:
                if st.button("Ver mi trayectoria 🚀"):
                    if st.session_state.answers[current] is None:
                        st.warning("Selecciona una respuesta antes de continuar.")
                    else:
                        st.session_state.page = "result"
                        st.rerun()
            else:
                if st.button("Siguiente ➜"):
                    if st.session_state.answers[current] is None:
                        st.warning("Selecciona una respuesta antes de continuar.")
                    else:
                        st.session_state.current_question += 1
                        st.rerun()


# ============================================================
# RESULTADO
# ============================================================

elif st.session_state.page == "result":

    result = calculate_result(
        questions,
        st.session_state.answers
    )

    profile = result["profile"]
    interest = result["interest"]
    outcome = result["outcome"]

    data = outcomes[outcome]

    profile_icon = PROFILE_ICONS.get(profile, "✨")
    interest_icon = INTEREST_ICONS.get(interest, "✨")

    profile_color = PROFILE_COLORS.get(profile, DEFAULT_ACCENT)
    interest_color = INTEREST_COLORS.get(interest, DEFAULT_ACCENT)

    st.balloons()

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        "<div class='eyebrow'>Tu resultado</div>",
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div class="hero-result" style="background:linear-gradient(135deg, {profile_color} 0%, {interest_color} 100%);">
        <div class="hero-icon">{profile_icon} {interest_icon}</div>
        <h2>{data["title"]}</h2>
        <p>{data["description"]}</p>
        <div class="tag-row">
            <div class="tag-pill" style="background:rgba(255,255,255,0.25);">Perfil: {profile}</div>
            <div class="tag-pill" style="background:rgba(255,255,255,0.25);">Interés: {interest}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("## 🧭 Posible trayectoria")
    st.markdown("<br>", unsafe_allow_html=True)

    if data["career"]:

        timeline_html = "<div class='timeline'>"
        for i, step in enumerate(data["career"]):
            timeline_html += (
                "<div class='timeline-item'>"
                f"<div class='timeline-node'>{i + 1}</div>"
                f"<div class='timeline-content'>{step}</div>"
                "</div>"
            )
        timeline_html += "</div>"

        st.markdown(timeline_html, unsafe_allow_html=True)

    else:
        st.info("Próximamente añadiremos esta trayectoria.")

    st.markdown("<br>", unsafe_allow_html=True)

    st.info(
        """
        Este resultado representa una posible trayectoria profesional basada en
        tus respuestas. No existe un único camino: cada persona puede desarrollar
        su carrera de muchas formas diferentes.
        """
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔄 Volver a realizar el cuestionario"):
        st.session_state.page = "welcome"
        st.session_state.current_question = 0
        st.session_state.answers = [None] * len(questions)
        st.rerun()
