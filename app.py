
import streamlit as st
from pathlib import Path

# ARCHIVOS DE PLANLY
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

# CONFIGURACIÓN DE LA PÁGINA
icono = str(FAVICON) if FAVICON.is_file() else "P"

st.set_page_config(
    page_title="PLANLY",
    page_icon=icono,
    layout="wide",
    initial_sidebar_state="expanded"
)

# DISEÑO Y TIPOGRAFÍA
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
    letter-spacing: 4px;
    color: var(--azul-oscuro) !important;
}

h2, h3 {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
    color: var(--azul-oscuro) !important;
}

p, label, li, input, button {
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
    transition: 0.2s;
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


# FUNCIONES
def mostrar_imagen(ruta, ancho=None):
    if ruta.is_file():
        st.image(str(ruta), width=ancho)
        return True
    return False


def nombre_imagen(archivo):
    return Path(archivo).stem.replace("_", " ")


# DATOS DE LA SESIÓN
if "favoritos" not in st.session_state:
    st.session_state.favoritos = []

if "planes" not in st.session_state:
    st.session_state.planes = []


# ENCABEZADO
col_logo, col_titulo = st.columns([1, 3])

with col_logo:
    mostrar_imagen(LOGO, ancho=180)

with col_titulo:
    st.title("PLANLY")
    st.subheader("Tus planes, a tu manera")
    st.write(
        "Descubrí ideas, organizá salidas y creá "
        "momentos especiales con quienes más querés."
    )

st.divider()


# PESTAÑAS PRINCIPALES
inicio, explorar, crear, favoritos = st.tabs([
    "Inicio",
    "Explorar",
    "Crear un plan",
    "Favoritos"
])


# INICIO
with inicio:
    col_texto, col_momi = st.columns([1.5, 1])

    with col_texto:
        st.header("Organizá algo especial")

        st.write(
            "Hola, soy MOMI. Voy a acompañarte para que "
            "organizar una salida sea fácil y divertido."
        )

        st.markdown("""
        <div class="plan-card">
            <h3>Tu próxima aventura empieza acá</h3>
            <p>Elegí una actividad, definí tu presupuesto
            y empezá a organizar tu plan.</p>
        </div>
        """, unsafe_allow_html=True)

        st.write("¿Qué te gustaría hacer?")
        st.write("Merendar, comer, tomar helado o pasear.")

        if st.button("Crear un plan", key="inicio_crear"):
            st.info(
                "Entrá en la pestaña Crear un plan "
                "para organizar tu salida."
            )

    with col_momi:
        if not mostrar_imagen(MOMI, ancho=300):
            st.info(
                "No encontramos la imagen de MOMI. "
                "Revisá el nombre del archivo."
            )

    st.subheader("Descubrí todo lo que podés hacer")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="plan-card">
            <h3>Explorar</h3>
            <p>Descubrí imágenes e ideas para inspirarte.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="plan-card">
            <h3>Organizar</h3>
            <p>Prepará una salida según tus preferencias.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="plan-card">
            <h3>Guardar</h3>
            <p>Conservá tus imágenes favoritas.</p>
        </div>
        """, unsafe_allow_html=True)

    if VIDEO.is_file():
        with st.expander("Ver presentación de Planly"):
            st.video(str(VIDEO))


# EXPLORAR
with explorar:
    st.header("Explorá Planly")

    st.write(
        "Recorré la galería y guardá las imágenes "
        "que más te gusten."
    )

    disponibles = [
        archivo for archivo in IMAGENES
        if (BASE_DIR / archivo).is_file()
    ]

    if not disponibles:
        st.warning(
            "No encontramos las imágenes. "
            "Comprobá que estén en la misma carpeta "
            "que aplicación.py y que los nombres coincidan."
        )
    else:
        st.caption(f"{len(disponibles)} imágenes disponibles")

        columnas = st.columns(3)

        for i, archivo in enumerate(disponibles):
            ruta = BASE_DIR / archivo

            with columnas[i % 3]:
                with st.container(border=True):
                    st.image(
                        str(ruta),
                        use_container_width=True
                    )

                    st.caption(nombre_imagen(archivo))

                    if archivo in st.session_state.favoritos:
                        st.button(
                            "Guardado",
                            key=f"guardado_{archivo}",
                            disabled=True,
                            use_container_width=True
                        )
                    else:
                        if st.button(
                            "Agregar a favoritos",
                            key=f"favorito_{archivo}",
                            use_container_width=True
                        ):
                            st.session_state.favoritos.append(archivo)
                            st.rerun()


# CREAR UN PLAN
with crear:
    st.header("Creá tu plan")

    st.write(
        "Completá los datos y prepará una salida "
        "a tu manera."
    )

    with st.form("formulario_plan"):
        zona = st.text_input(
            "¿En qué zona quieren salir?",
            placeholder="Ejemplo: Lanús"
        )

        actividad = st.selectbox(
            "¿Qué quieren hacer?",
            [
                "Merendar",
                "Comer",
                "Tomar helado",
                "Pasear"
            ]
        )

        presupuesto = st.number_input(
            "Presupuesto total en pesos",
            min_value=0,
            value=10000,
            step=1000
        )

        personas = st.number_input(
            "¿Cuántas personas son?",
            min_value=1,
            value=2,
            step=1
        )

        enviar = st.form_submit_button(
            "Preparar mi plan",
            use_container_width=True
        )

    if enviar:
        if not zona.strip():
            st.warning("Primero ingresá la zona.")
        else:
            plan = {
                "zona": zona.strip(),
                "actividad": actividad,
                "presupuesto": presupuesto,
                "personas": personas
            }

            st.session_state.planes.append(plan)

            st.success("Tu plan quedó organizado.")

            c1, c2 = st.columns(2)

            with c1:
                st.markdown("**Zona**")
                st.write(zona.strip())

                st.markdown("**Actividad**")
                st.write(actividad)

            with c2:
                st.markdown("**Presupuesto total**")
                st.write(f"${presupuesto:,.0f}")

                st.markdown("**Cantidad de personas**")
                st.write(personas)

            st.info(
                "Esta versión organiza tus preferencias, "
                "pero todavía no busca lugares reales "
                "ni comprueba precios o disponibilidad."
            )

    if st.session_state.planes:
        st.divider()
        st.subheader("Planes de esta sesión")

        for numero, plan in enumerate(
            reversed(st.session_state.planes),
            start=1
        ):
            with st.container(border=True):
                st.write(
                    f"**Plan {numero}: {plan['actividad']}**"
                )
                st.write(f"Zona: {plan['zona']}")
                st.write(
                    f"Presupuesto: ${plan['presupuesto']:,.0f}"
                )
                st.write(
                    f"Personas: {plan['personas']}"
                )


# FAVORITOS
with favoritos:
    st.header("Tus favoritos")

    st.write(
        "Acá aparecen las imágenes que guardaste "
        "desde la galería."
    )

    if not st.session_state.favoritos:
        st.info(
            "Todavía no guardaste imágenes. "
            "Entrá en Explorar para elegir tus favoritas."
        )
    else:
        for archivo in list(st.session_state.favoritos):
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
                    st.write(nombre_imagen(archivo))

                    if st.button(
                        "Quitar de favoritos",
                        key=f"quitar_{archivo}"
                    ):
                        st.session_state.favoritos.remove(archivo)
                        st.rerun()


# PIE DE PÁGINA
st.divider()

st.markdown(
    "<p style='text-align:center; color:#64748B;'>"
    "PLANLY | Creá momentos que valgan la pena."
    "</p>",
    unsafe_allow_html=True
)
