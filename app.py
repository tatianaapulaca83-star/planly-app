@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Poppins:wght@400;500;600;700&display=swap');
from pathlib import Path

# ==========================================
# PLANLY - Aplicación principal
# ==========================================

BASE_DIR = Path(__file__).parent

LOGO = BASE_DIR / "1791589153613.jpg"
MOMI = BASE_DIR / "IMG_20261011_113224.png"
FAVICON = BASE_DIR / "file_00000000ae90820eab984a0a71702a6d.png"
VIDEO = BASE_DIR / "Vídeo sin título.mp4"

IMAGENES = [
    "IMG_20261011_112641.png",
    "IMG_20261011_112704.png",
    "IMG_20261011_112715.png",
    "IMG_20261011_112740.png",
    "IMG_20261011_112808.png",
    "IMG_20261011_112829.png",
    "IMG_20261011_112853.png",
    "IMG_20261011_112958.png",
    "IMG_20261011_113026.png",
    "IMG_20261011_113046.png",
    "IMG_20261011_113107.png",
    "IMG_20261011_113123.png",
    "IMG_20261011_113141.png",
    "IMG_20261011_113156.png",
    "IMG_20261011_113210.png",
]

icono = str(FAVICON) if FAVICON.is_file() else "🦦"

st.set_page_config(
    page_title="Planly",
    page_icon=icono,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# DISEÑO
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700;800&family=Poppins:wght@400;500;600;700&display=swap');

:root {
    --azul: #2563EB;
    --azul-oscuro: #1D4ED8;
    --azul-claro: #EFF6FF;
    --borde: #DBEAFE;
    --texto: #334155;
}

.stApp {
    background: #F8FAFF;
    color: var(--texto);
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1 {
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 800 !important;
    text-transform: uppercase;
    letter-spacing: 5px;
    color: var(--azul-oscuro) !important;
}

h2, h3 {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
    color: var(--azul-oscuro) !important;
}

p, label, li, button, input {
    font-family: 'Poppins', sans-serif;
}

[data-testid="stSidebar"] {
    background: var(--azul-claro);
    border-right: 1px solid var(--borde);
}

div.stButton > button,
div.stFormSubmitButton > button {
    background: var(--azul);
    color: white;
    border: 1px solid var(--azul);
    border-radius: 12px;
    min-height: 44px;
    font-family: 'Poppins', sans-serif;
    font-weight: 500;
}

div.stButton > button:hover,
div.stFormSubmitButton > button:hover {
    background: var(--azul-oscuro);
    color: white;
    border-color: var(--azul-oscuro);
}

div[data-testid="stForm"] {
    background: white;
    border: 1px solid var(--borde);
    border-radius: 18px;
    padding: 24px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--borde);
    border-radius: 16px;
}

.stTabs [aria-selected="true"] {
    color: var(--azul) !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background: var(--azul) !important;
}

.plan-card {
    background: white;
    border: 1px solid var(--borde);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 14px;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)



# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

def mostrar_imagen(ruta, ancho=None):
    """Muestra una imagen si el archivo existe."""
    if ruta.is_file():
        st.image(str(ruta), width=ancho)
        return True
    return False


def nombre_lugar(archivo):
    """Crea un nombre legible a partir del archivo."""
    return Path(archivo).stem.replace("_", " ")


# ==========================================
# ESTADO DE LA APLICACIÓN
# ==========================================

if "favoritos" not in st.session_state:
    st.session_state.favoritos = []

if "planes" not in st.session_state:
    st.session_state.planes = []


# ==========================================
# CABECERA
# ==========================================

col_logo, col_titulo = st.columns([1, 3])

with col_logo:
    mostrar_imagen(LOGO, ancho=190)

with col_titulo:
    st.title("Planly")
    st.subheader("Tus planes, a tu manera")
    st.write(
        "Descubrí ideas, organizá salidas y creá "
        "momentos especiales con quienes más querés. 💗"
    )

st.divider()

# ==========================================
# NAVEGACIÓN
# ==========================================

inicio, explorar, crear, favoritos = st.tabs([
    "🏡 Inicio",
    "📍 Explorar",
    "✨ Crear un plan",
    "💗 Favoritos"
])

# ==========================================
# INICIO
# ==========================================

with inicio:
    col_texto, col_momi = st.columns([1.5, 1])

    with col_texto:
        st.markdown("## ¡Hola! ¿Qué hacemos hoy?")
        st.write(
            "¡Soy MOMI! 🦦 Voy a acompañarte para que "
            "organizar una salida sea fácil y divertido."
        )

        st.markdown(
            '<div class="plan-card">'
            '<h3>🌷 Tu próxima aventura empieza acá</h3>'
            '<p>Elegí una actividad, definí tu presupuesto '
            'y empezá a organizar tu plan.</p>'
            '</div>',
            unsafe_allow_html=True
        )

        st.write("**¿Qué te gustaría hacer?**")
        st.caption(
            "Merendar · Comer · Tomar helado · Pasear"
        )

    with col_momi:
        if not mostrar_imagen(MOMI, ancho=300):
            st.info(
                "Todavía no encontramos el archivo de MOMI. "
                "Revisá el nombre y la ubicación en GitHub."
            )

    st.markdown("### 💗 Tu espacio Planly")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            '<div class="plan-card">'
            '<h3>📍 Explorar</h3>'
            '<p>Recorré nuestra galería de imágenes.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            '<div class="plan-card">'
            '<h3>✨ Organizar</h3>'
            '<p>Prepará una salida a tu manera.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            '<div class="plan-card">'
            '<h3>💗 Guardar</h3>'
            '<p>Conservá tus imágenes favoritas.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    if VIDEO.is_file():
        with st.expander("🎬 Ver el video de Planly"):
            st.video(str(VIDEO))

# ==========================================
# EXPLORAR
# ==========================================

with explorar:
    st.header("📍 Explorá Planly")
    st.write(
        "Acá podés ver las imágenes que subiste "
        "a tu repositorio."
    )

    imagenes_disponibles = [
        archivo for archivo in IMAGENES
        if (BASE_DIR / archivo).is_file()
    ]

    if not imagenes_disponibles:
        st.warning(
            "No encontramos las imágenes de la galería. "
            "Comprobá que los archivos estén junto a "
            "aplicación.py y que sus nombres coincidan."
        )
    else:
        st.caption(
            f"{len(imagenes_disponibles)} imágenes disponibles"
        )

        columnas = st.columns(3)

        for i, archivo in enumerate(imagenes_disponibles):
            ruta = BASE_DIR / archivo

            with columnas[i % 3]:
                with st.container(border=True):
                    st.image(str(ruta), use_container_width=True)
                    st.caption(nombre_lugar(archivo))

                    if archivo in st.session_state.favoritos:
                        st.button(
                            "💗 Guardado",
                            key=f"guardado_{archivo}",
                            disabled=True,
                            use_container_width=True
                        )
                    else:
                        if st.button(
                            "♡ Agregar a favoritos",
                            key=f"favorito_{archivo}",
                            use_container_width=True
                        ):
                            st.session_state.favoritos.append(archivo)
                            st.rerun()

# ==========================================
# CREAR UN PLAN
# ==========================================

with crear:
    st.header("✨ Organicemos tu salida")
    st.write("Completá los datos para preparar tu plan.")

    with st.form("formulario_plan"):
        zona = st.text_input(
            "📍 ¿En qué zona quieren salir?",
            placeholder="Ejemplo: Lanús"
        )

        actividad = st.selectbox(
            "🎉 ¿Qué quieren hacer?",
            [
                "Merendar",
                "Comer",
                "Tomar helado",
                "Pasear"
            ]
        )

        presupuesto = st.number_input(
            "💰 Presupuesto total en pesos",
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

        enviar = st.form_submit_button(
            "✨ Preparar mi plan",
            use_container_width=True
        )

    if enviar:
        if not zona.strip():
            st.warning("MOMI necesita saber la zona.")
        else:
            plan = {
                "zona": zona.strip(),
                "actividad": actividad,
                "presupuesto": presupuesto,
                "personas": personas
            }

            st.session_state.planes.append(plan)

            st.success("¡Tu plan ya está organizado! 💗")

            c1, c2 = st.columns(2)

            with c1:
                st.markdown("**📍 Zona**")
                st.write(zona.strip())

                st.markdown("**🎉 Actividad**")
                st.write(actividad)

            with c2:
                st.markdown("**💰 Presupuesto total**")
                st.write(f"${presupuesto:,.0f}")

                st.markdown("**👥 Personas**")
                st.write(personas)

            st.info(
                "Este es tu plan inicial. Todavía no buscamos "
                "lugares reales ni verificamos precios o "
                "disponibilidad."
            )

    if st.session_state.planes:
        st.divider()
        st.subheader("🗓️ Planes de esta sesión")

        for numero, plan in enumerate(
            reversed(st.session_state.planes), start=1
        ):
            with st.container(border=True):
                st.write(f"**Plan {numero}: {plan['actividad']}**")
                st.write(f"📍 {plan['zona']}")
                st.write(f"💰 ${plan['presupuesto']:,.0f}")
                st.write(f"👥 {plan['personas']} personas")

# ==========================================
# FAVORITOS
# ==========================================

with favoritos:
    st.header("💗 Tus favoritos")
    st.write("Guardá las imágenes que más te gusten.")

    if not st.session_state.favoritos:
        st.info(
            "Todavía no tenés favoritos. "
            "Entrá en Explorar y guardá alguna imagen. 🦦"
        )
    else:
        for archivo in st.session_state.favoritos:
            ruta = BASE_DIR / archivo

            with st.container(border=True):
                col_imagen, col_info = st.columns([1, 2])

                with col_imagen:
                    if ruta.is_file():
                        st.image(
                            str(ruta),
                            use_container_width=True
                        )

                with col_info:
                    st.write(nombre_lugar(archivo))

                    if st.button(
                        "Quitar de favoritos",
                        key=f"quitar_{archivo}"
                    ):
                        st.session_state.favoritos.remove(archivo)
                        st.rerun()

# ==========================================
# PIE DE PÁGINA
# ==========================================

st.divider()

st.markdown(
    "<p style='text-align:center; color:#81758e;'>"
    "Planly 💗 Creá momentos que valgan la pena. 🦦"
    "</p>",
    unsafe_allow_html=True
)
