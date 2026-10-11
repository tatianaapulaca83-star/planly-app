import streamlit as st

st.set_page_config(
    page_title="Planly",
    page_icon="🦦",
    layout="centered"
)

st.title("🦦 Planly")
st.subheader("¡Armemos un plan genial!")
st.write("Hola, soy MOMI. Te ayudo a organizar tu próxima salida 💗")

st.divider()

st.header("✨ Creemos tu plan")

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

if st.button("🔎 Buscar mi plan", use_container_width=True):
    if not zona.strip():
        st.warning("¡MOMI necesita saber en qué zona buscar!")
    else:
        st.success("¡Vamos a organizar tu salida!")
        st.write("📍 Zona:", zona)
        st.write("🎉 Actividad:", actividad)
        st.write("💰 Presupuesto total:", f"${presupuesto:,.0f}")
        st.write("👥 Personas:", personas)
        st.info(
            "Esta es la primera versión de Planly. "
            "El siguiente paso será conectar lugares reales."
        )

st.caption("Planly 💗 Creá momentos que valgan la pena.")
