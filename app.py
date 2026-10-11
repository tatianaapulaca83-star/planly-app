import streamlit as st

st.set_page_config(st.image("1791589153613.jpg", width=220)

st.title("Planly")
st.subheader("Tus planes, a tu manera")

col1, col2 = st.columns([2, 1])

with col1:
    st.write(
        "¡Hola! Soy MOMI y te ayudo a organizar "
        "salidas para crear momentos especiales. 💗"
    )

with col2:
    st.image("IMG_20261011_113224.png", width=180)

st.divider()
    page_title="Planly",
    page_icon="file_00000000ae90820eab984a0a71702a6d.png",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg, #fff5f8 0%, #f7f3ff 55%, #effaf5 100%
    );
    color: #39365f;
}
.block-container {
    max-width: 760px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}
h1, h2, h3 {
    color: #514477 !important;
}
.intro {
    background: rgba(255,255,255,0.82);
    border: 1px solid #eee3ff;
    border-radius: 24px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 5px 20px #51447710;
}
.momi {
    font-size: 68px;
    margin-bottom: 0;
}
.subtitle {
    color: #75658f;
    font-size: 18px;
}
div[data-testid="stForm"] {
    background: rgba(255,255,255,0.88);
    border: 1px solid #eadfff;
    border-radius: 22px;
    padding: 22px;
}
.stButton > button {
    background: linear-gradient(90deg, #bca0e8, #d6b5e8);
    color: white;
    border: none;
    border-radius: 16px;
    min-height: 48px;
    font-weight: 600;
}
.stButton > button:hover {
    border: 1px solid #9d7dd4;
    color: #514477;
}
div[data-baseweb="input"],
div[data-baseweb="select"] {
    border-radius: 12px;
}
.footer {
    text-align: center;
    color: #8877a4;
    font-size: 14px;
    padding-top: 22px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="intro">
    <div class="momi">🦦🗺️</div>
    <h1>Planly</h1>
    <div class="subtitle">Tus planes, a tu manera 💗</div>
    <p>¡Hola! Soy MOMI. Te ayudo a organizar tu próxima salida.</p>
</div>
""", unsafe_allow_html=True)

st.write("")

st.header("✨ Creemos tu plan")
st.write("Contame qué tienen ganas de hacer y armamos una salida.")

with st.form("formulario_plan"):
    zona = st.text_input(
        "📍 ¿En qué zona quieren salir?",
        placeholder="Ejemplo: Lanús"
    )

    actividad = st.selectbox(
        "🎉 ¿Qué quieren hacer?",
        ["Merendar", "Comer", "Tomar helado", "Pasear"]
    )

    presupuesto = st.number_input(
        "💰 ¿Cuánto quieren gastar en total?",
        min_value=0,
        value=10000,
        step=1000
    )

    personas = st.number_input(
        "👥 ¿Cuántas personas son?",
        min_value=1,
        value=2,
        step=1
    )

    buscar = st.form_submit_button(
        "🔎 Buscar mi plan",
        use_container_width=True
    )

if buscar:
    if not zona.strip():
        st.warning("¡MOMI necesita saber en qué zona buscar! 🦦")
    else:
        st.success("¡Ya tenemos los datos de tu salida! 💗")

        st.subheader("🌷 Tu plan")
        st.write(f"📍 **Zona:** {zona.strip()}")
        st.write(f"🎉 **Actividad:** {actividad}")
        st.write(f"💰 **Presupuesto total:** ${presupuesto:,.0f}")
        st.write(f"👥 **Personas:** {personas}")

        st.info(
            "MOMI está preparando nuevas formas de encontrar "
            "lugares para vos. Próximamente conectaremos lugares reales."
        )

st.markdown("""
<div class="footer">
    Planly 💗 Creá momentos que valgan la pena.
</div>
""", unsafe_allow_html=True)
