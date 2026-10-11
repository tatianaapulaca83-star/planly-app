
import streamlit as st
from pathlib import Path
from datetime import date, timedelta
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import URLError
import json

# =========================================================
# 1. CONFIGURACIÓN
# =========================================================

CARPETA = Path(__file__).parent

MOMI = "IMG_20261011_113224.png"
FAVICON = "file_00000000ae90820eab984a0a71702a6d.png"
VIDEO = "Vídeo sin título.mp4"

IMAGENES_EXTRA = [
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

icono = CARPETA / FAVICON

st.set_page_config(
    page_title="Planly | Tu próxima salida",
    page_icon=str(icono) if icono.exists() else "💙",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# 2. ESTILO VISUAL
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Poppins:wght@300;400;500;600;700&display=swap');

:root {
    --azul: #2563EB;
    --azul-oscuro: #173B7A;
    --celeste: #EFF6FF;
    --fondo: #F8FAFF;
    --texto: #263650;
    --suave: #64748B;
    --borde: #DCE6F8;
}

.stApp {
    background: var(--fondo);
    color: var(--texto);
    font-family: 'Poppins', sans-serif;
}

h1, h2, h3 {
    font-family: 'Montserrat', sans-serif !important;
    color: var(--azul-oscuro);
}

.block-container {
    max-width: 1180px;
    padding-top: 1.6rem;
    padding-bottom: 3rem;
}

.hero {
    background: linear-gradient(135deg, #EAF2FF, #FFFFFF);
    border: 1px solid var(--borde);
    border-radius: 28px;
    padding: 32px;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: clamp(2.5rem, 6vw, 4.2rem);
    letter-spacing: 4px;
    font-weight: 800;
    margin: 0;
    color: var(--azul-oscuro);
}

.hero p {
    color: #536783;
    font-size: 1rem;
    margin-bottom: 0;
}

.section-card {
    background: white;
    border: 1px solid var(--borde);
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 16px;
}

.small-note {
    color: var(--suave);
    font-size: 0.88rem;
}

div[data-testid="stTabs"] button {
    font-weight: 600;
}

.stButton > button,
.stLinkButton > a,
.stFormSubmitButton > button {
    border-radius: 12px;
    font-weight: 600;
    min-height: 43px;
}

.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background: var(--azul);
    border-color: var(--azul);
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid var(--borde);
    border-radius: 16px;
    padding: 14px;
}

div[data-testid="stAlert"] {
    border-radius: 14px;
}

hr {
    border-color: var(--borde);
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 2.1. AUTENTICACIÓN CON FIREBASE
# =========================================================

import requests

FIREBASE_API_KEY = st.secrets["firebase"]["api_key"]
FIREBASE_PROJECT_ID = st.secrets["firebase"]["project_id"]

URL_AUTH = (
    "https://identitytoolkit.googleapis.com/v1/accounts"
)


def autenticar_firebase(modo, email, password):
    endpoints = {
        "registro": "signUp",
        "login": "signInWithPassword",
    }

    url = (
        f"{URL_AUTH}:{endpoints[modo]}"
        f"?key={FIREBASE_API_KEY}"
    )

    try:
        respuesta = requests.post(
            url,
            json={
                "email": email,
                "password": password,
                "returnSecureToken": True,
            },
            timeout=15,
        )

        datos = respuesta.json()

        if respuesta.ok:
            st.session_state.firebase_user = {
                "uid": datos["localId"],
                "email": datos["email"],
                "id_token": datos["idToken"],
                "refresh_token": datos["refreshToken"],
            }
            return True, ""

        codigo = datos.get("error", {}).get("message", "")

        if codigo.startswith("WEAK_PASSWORD"):
            return False, "La contraseña debe tener al menos 6 caracteres."

        mensajes = {
            "EMAIL_EXISTS": "Ese correo ya tiene una cuenta.",
            "INVALID_EMAIL": "El correo no es válido.",
            "INVALID_LOGIN_CREDENTIALS": "El correo o la contraseña son incorrectos.",
            "TOO_MANY_ATTEMPTS_TRY_LATER": "Demasiados intentos. Probá más tarde.",
        }

        return False, mensajes.get(
            codigo,
            "No pudimos completar la operación. Revisá los datos e intentá nuevamente.",
        )

    except requests.RequestException:
        return False, "No pudimos conectar con Firebase. Intentá nuevamente."
    url = (
        f"{URL_AUTH}:{endpoints[modo]}"
        f"?key={FIREBASE_API_KEY}"
    )

    try:
        respuesta = requests.post(
            url,
            json={
                "email": email,
                "password": password,
                "returnSecureToken": True,
            },
            timeout=15,
        )

        datos = respuesta.json()

        if respuesta.ok:
            st.session_state.firebase_user = {
                "uid": datos["localId"],
                "email": datos["email"],
                "id_token": datos["idToken"],
                "refresh_token": datos["refreshToken"],
            }
            return True, ""

        codigo = datos.get("error", {}).get("message", "")
        mensajes = {
            "EMAIL_EXISTS": "Ese correo ya tiene una cuenta.",
            "INVALID_EMAIL": "El correo no es válido.",
            "INVALID_LOGIN_CREDENTIALS":
                "El correo o la contraseña son incorrectos.",
            "WEAK_PASSWORD : Password should be at least 6 characters":
                "La contraseña debe tener al menos 6 caracteres.",
            "TOO_MANY_ATTEMPTS_TRY_LATER":
                "Demasiados intentos. Probá más tarde.",
        }

        if codigo.startswith("WEAK_PASSWORD"):
            return False, "La contraseña debe tener al menos 6 caracteres."

        return False, mensajes.get(
            codigo,
            "No pudimos completar la operación. Revisá los datos e intentá nuevamente.",
        )

    except requests.RequestException:
        return False, "No pudimos conectar con Firebase. Intentá nuevamente."


# Mostrar acceso antes de entrar a Planly
if "firebase_user" not in st.session_state:
    st.session_state.firebase_user = None

if not st.session_state.firebase_user:
    st.markdown("## Bienvenido/a a Planly")
    st.write("Ingresá a tu cuenta o creá una nueva para comenzar.")

    pesta_login, pesta_registro = st.tabs(
        ["Iniciar sesión", "Crear cuenta"]
    )

    with pesta_login:
        with st.form("firebase_login"):
            email_login = st.text_input("Correo electrónico")
            password_login = st.text_input(
                "Contraseña",
                type="password",
            )
            enviar_login = st.form_submit_button(
                "Iniciar sesión",
                type="primary",
                use_container_width=True,
            )

        if enviar_login:
            if not email_login.strip() or not password_login:
                st.warning("Completá el correo y la contraseña.")
            else:
                correcto, mensaje = autenticar_firebase(
                    "login",
                    email_login.strip(),
                    password_login,
                )
                if correcto:
                    st.rerun()
                else:
                    st.error(mensaje)

    with pesta_registro:
        with st.form("firebase_registro"):
            email_registro = st.text_input(
                "Tu correo electrónico",
                key="registro_email",
            )
            password_registro = st.text_input(
                "Creá una contraseña (mínimo 6 caracteres)",
                type="password",
                key="registro_password",
            )
            confirmar_password = st.text_input(
                "Confirmá tu contraseña",
                type="password",
            )
            enviar_registro = st.form_submit_button(
                "Crear mi cuenta",
                type="primary",
                use_container_width=True,
            )

        if enviar_registro:
            if not email_registro.strip() or not password_registro:
                st.warning("Completá todos los campos.")
            elif password_registro != confirmar_password:
                st.error("Las contraseñas no coinciden.")
            elif len(password_registro) < 6:
                st.error("La contraseña debe tener al menos 6 caracteres.")
            else:
                correcto, mensaje = autenticar_firebase(
                    "registro",
                    email_registro.strip(),
                    password_registro,
                )
                if correcto:
                    st.rerun()
                else:
                    st.error(mensaje)

    st.stop()

# =========================================================
# GUARDADO DE PLANES Y FAVORITOS EN FIRESTORE
# =========================================================

import json


def obtener_url_firestore():
    usuario = st.session_state.firebase_user
    uid = usuario["uid"]

    return (
        "https://firestore.googleapis.com/v1/projects/"
        f"{FIREBASE_PROJECT_ID}/databases/(default)/documents/"
        f"users/{uid}/data/app"
    )


def cargar_datos_firestore():
    usuario = st.session_state.firebase_user

    respuesta = requests.get(
        obtener_url_firestore(),
        headers={
            "Authorization": f"Bearer {usuario['id_token']}"
        },
        timeout=15,
    )

    # Si todavía no hay documento, empezamos con listas vacías.
    if respuesta.status_code == 404:
        return [], []

    respuesta.raise_for_status()

    campos = respuesta.json().get("fields", {})

    planes = json.loads(
        campos.get("planes_json", {}).get("stringValue", "[]")
    )

    favoritos = json.loads(
        campos.get("favoritos_json", {}).get("stringValue", "[]")
    )

    return planes, favoritos


def guardar_datos_firestore(planes, favoritos):
    usuario = st.session_state.firebase_user

    datos = {
        "fields": {
            "planes_json": {
                "stringValue": json.dumps(
                    planes, ensure_ascii=False
                )
            },
            "favoritos_json": {
                "stringValue": json.dumps(
                    favoritos, ensure_ascii=False
                )
            },
        }
    }

    respuesta = requests.patch(
        obtener_url_firestore(),
        params=[
            ("updateMask.fieldPaths", "planes_json"),
            ("updateMask.fieldPaths", "favoritos_json"),
        ],
        headers={
            "Authorization": f"Bearer {usuario['id_token']}",
            "Content-Type": "application/json",
        },
        json=datos,
        timeout=15,
    )

    respuesta.raise_for_status()

# =========================================================
# 3. CATEGORÍAS Y OPCIONES
# =========================================================

CATEGORIAS = {
    "Merendar o tomar café": "cafeterías y lugares para merendar",
    "Comer": "restaurantes",
    "Tomar helado": "heladerías",
    "Pasear": "parques y paseos",
    "Ir al cine": "cines",
    "Hacer compras": "centros comerciales y tiendas",
    "Actividades al aire libre": "actividades al aire libre",
    "Actividades bajo techo": "actividades bajo techo",
    "Salir con amigos": "actividades para hacer con amigos",
    "Otra actividad": "lugares y actividades para salir",
}

TRANSPORTES = [
    "Caminando",
    "Colectivo",
    "Tren",
    "Auto",
    "Transporte por aplicación",
    "Todavía no lo sé",
]

PREFERENCIAS = [
    "Económico",
    "Tranquilo",
    "Al aire libre",
    "Bajo techo",
    "Familiar",
    "Con amigos",
    "Romántico",
    "Indistinto",
]

def archivo(nombre):
    return CARPETA / nombre

def buscar_maps(consulta):
    parametros = urlencode({
        "api": "1",
        "query": consulta,
    })
    return "https://www.google.com/maps/search/?" + parametros

def crear_ruta(destino, transporte):
    modos = {
        "Caminando": "walking",
        "Colectivo": "transit",
        "Tren": "transit",
        "Auto": "driving",
        "Transporte por aplicación": "driving",
        "Todavía no lo sé": "driving",
    }

    parametros = urlencode({
        "api": "1",
        "destination": destino,
        "travelmode": modos.get(transporte, "driving"),
    })
    return "https://www.google.com/maps/dir/?" + parametros

def dinero(valor):
    return "$" + f"{valor:,.0f}".replace(",", ".")

def guardar_favorito(nombre, zona, categoria):
    nombre = nombre.strip()
    zona = zona.strip()

    if not nombre:
        return False

    for favorito in st.session_state.favoritos:
        if (
            favorito["nombre"].casefold() == nombre.casefold()
            and favorito["zona"].casefold() == zona.casefold()
        ):
            return False

    st.session_state.favoritos.append({
        "nombre": nombre,
        "zona": zona,
        "categoria": categoria,
        "url": buscar_maps(f"{nombre}, {zona}"),
    })
    return True

# =========================================================
# 4. CONSULTA DEL CLIMA
# =========================================================

def consultar_clima(zona, fecha_salida):
    try:
        parametros = urlencode({
            "name": zona,
            "count": 1,
            "language": "es",
            "format": "json",
        })

        url_geo = (
            "https://geocoding-api.open-meteo.com/v1/search?"
            + parametros
        )

        with urlopen(url_geo, timeout=8) as respuesta:
            geografia = json.loads(
                respuesta.read().decode("utf-8")
            )

        resultados = geografia.get("results", [])

        if not resultados:
            return {
                "error": "No encontramos esa zona. Probá con una localidad o ciudad."
            }

        lugar = resultados[0]
        latitud = lugar["latitude"]
        longitud = lugar["longitude"]

        parametros_clima = urlencode({
            "latitude": latitud,
            "longitude": longitud,
            "daily": (
                "weather_code,temperature_2m_max,"
                "temperature_2m_min,precipitation_probability_max"
            ),
            "timezone": "auto",
            "start_date": fecha_salida.isoformat(),
            "end_date": fecha_salida.isoformat(),
        })

        url_clima = (
            "https://api.open-meteo.com/v1/forecast?"
            + parametros_clima
        )

        with urlopen(url_clima, timeout=8) as respuesta:
            clima = json.loads(
                respuesta.read().decode("utf-8")
            )

        daily = clima.get("daily", {})

        if not daily.get("time"):
            return {
                "error": "No hay pronóstico disponible para esa fecha."
            }

        codigo = daily["weather_code"][0]

        descripciones = {
            0: ("Despejado", "☀️"),
            1: ("Mayormente despejado", "🌤️"),
            2: ("Parcialmente nublado", "⛅"),
            3: ("Nublado", "☁️"),
            45: ("Niebla", "🌫️"),
            48: ("Niebla", "🌫️"),
            51: ("Llovizna leve", "🌦️"),
            53: ("Llovizna", "🌦️"),
            55: ("Llovizna intensa", "🌧️"),
            61: ("Lluvia leve", "🌦️"),
            63: ("Lluvia", "🌧️"),
            65: ("Lluvia intensa", "🌧️"),
            71: ("Nieve leve", "🌨️"),
            73: ("Nieve", "🌨️"),
            75: ("Nieve intensa", "❄️"),
            80: ("Chaparrones leves", "🌦️"),
            81: ("Chaparrones", "🌧️"),
            82: ("Chaparrones intensos", "⛈️"),
            95: ("Tormenta", "⛈️"),
            96: ("Tormenta con granizo", "⛈️"),
            99: ("Tormenta intensa", "⛈️"),
        }

        descripcion, emoji = descripciones.get(
            codigo, ("Estado variable", "🌥️")
        )

        lluvia = daily.get(
            "precipitation_probability_max", [None]
        )[0]

        return {
            "lugar": lugar.get("name", zona),
            "descripcion": descripcion,
            "emoji": emoji,
            "max": daily["temperature_2m_max"][0],
            "min": daily["temperature_2m_min"][0],
            "lluvia": lluvia,
        }

    except (
        URLError,
        TimeoutError,
        ValueError,
        KeyError,
        IndexError,
        OSError,
    ):
        return {
            "error": "No pudimos consultar el clima. "
                     "Revisá tu conexión e intentá nuevamente."
        }

# =========================================================
# 5. ESTADO DE LA APLICACIÓN
# =========================================================

if "favoritos" not in st.session_state:
    st.session_state.favoritos = []

if "planes" not in st.session_state:
    st.session_state.planes = []

if "busqueda_actual" not in st.session_state:
    st.session_state.busqueda_actual = None

if "plan_actual" not in st.session_state:
    st.session_state.plan_actual = None
    
# =========================================================
# 5.1. CARGAR LOS DATOS DEL USUARIO DESDE FIRESTORE
# =========================================================

if (
    st.session_state.get("firebase_user")
    and not st.session_state.get("firestore_cargado", False)
):
    try:
        planes_guardados, favoritos_guardados = (
            cargar_datos_firestore()
        )

        st.session_state.planes = planes_guardados
        st.session_state.favoritos = favoritos_guardados
        st.session_state.firestore_cargado = True

    except Exception:
        st.warning(
            "No pudimos cargar tus datos guardados. "
            "Revisá tu conexión e intentá nuevamente."
        )


# =========================================================
# 6. ENCABEZADO SIN LOGO
# =========================================================

st.markdown("""
<div class="hero">
    <h1>PLANLY</h1>
    <p>Encontrá tu próximo lugar favorito.</p>
    <p>Ideas para salir, compartir y disfrutar a tu manera.</p>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 7. PESTAÑAS
# =========================================================

inicio, explorar, crear, favoritos = st.tabs([
    "🏠 Inicio",
    "🧭 Explorar",
    "✨ Crear un plan",
    "💙 Favoritos",
])

# =========================================================
# 8. INICIO
# =========================================================

with inicio:
    st.markdown("## Tu próxima salida empieza acá")

    st.write(
        "Descubrí lugares, organizá salidas y encontrá opciones "
        "que se adapten a tus gustos y a tu presupuesto."
    )

    col_texto, col_momi = st.columns(
        [1.15, 1],
        gap="large",
        vertical_alignment="center",
    )

    with col_texto:
        st.markdown("""
        <div class="section-card">
            <h3>¿Qué tenés ganas de hacer?</h3>
            <p>☕ Descubrir cafeterías y meriendas</p>
            <p>🍦 Encontrar heladerías</p>
            <p>🌳 Conocer parques y paseos</p>
            <p>🎬 Buscar actividades para compartir</p>
            <p>💸 Organizar gastos y alternativas</p>
        </div>
        """, unsafe_allow_html=True)

        st.info(
            "Elegí «Explorar» para buscar lugares o "
            "«Crear un plan» para organizar tu salida."
        )

    with col_momi:
        if archivo(MOMI).exists():
            st.image(
                str(archivo(MOMI)),
                use_container_width=True,
            )
        else:
            st.markdown("## ¡Hola! Soy MOMI 💙")
            st.write(
                "Tu compañero para descubrir lugares y organizar salidas."
            )

    st.markdown("---")
    st.markdown("### Tu espacio de ideas")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Planes creados",
        len(st.session_state.planes),
    )

    c2.metric(
        "Favoritos",
        len(st.session_state.favoritos),
    )

    c3.metric(
        "Próxima aventura",
        "¡A descubrir!",
    )

    if archivo(VIDEO).exists():
        with st.expander("Ver video de Planly"):
            st.video(str(archivo(VIDEO)))

    disponibles = [
        nombre for nombre in IMAGENES_EXTRA
        if archivo(nombre).exists()
    ]

    if disponibles:
        with st.expander("Ver galería de imágenes de Planly"):
            columnas = st.columns(3)

            for i, nombre in enumerate(disponibles):
                with columnas[i % 3]:
                    st.image(
                        str(archivo(nombre)),
                        use_container_width=True,
                    )

# =========================================================
# 9. EXPLORAR
# =========================================================

with explorar:
    st.markdown("## Explorá lugares")
    st.write(
        "Buscá sitios reales según la zona y la actividad que prefieras."
    )

    with st.form("form_explorar"):
        zona_explorar = st.text_input(
            "¿En qué zona querés buscar?",
            placeholder="Ej.: Lanús, Banfield, Lomas de Zamora",
        )

        categoria_explorar = st.selectbox(
            "¿Qué te gustaría hacer?",
            list(CATEGORIAS.keys()),
        )

        buscar = st.form_submit_button(
            "Buscar lugares",
            type="primary",
            use_container_width=True,
        )

    if buscar:
        if not zona_explorar.strip():
            st.warning("Primero escribí una zona.")
        else:
            st.session_state.busqueda_actual = {
                "zona": zona_explorar.strip(),
                "categoria": categoria_explorar,
                "consulta": (
                    f"{CATEGORIAS[categoria_explorar]}, "
                    f"{zona_explorar.strip()}, Argentina"
                ),
            }

    busqueda = st.session_state.busqueda_actual

    if busqueda:
        st.markdown("### Opciones para descubrir")

        st.write(
            f"Buscando **{busqueda['categoria'].lower()}** en "
            f"**{busqueda['zona']}**."
        )

        st.link_button(
            "📍 Ver resultados en Google Maps",
            buscar_maps(busqueda["consulta"]),
            use_container_width=True,
        )

        st.components.v1.iframe(
            "https://maps.google.com/maps?"
            + urlencode({
                "q": busqueda["consulta"],
                "output": "embed",
            }),
            height=350,
            scrolling=False,
        )

        st.caption(
            "Los resultados, horarios, precios y ubicaciones "
            "dependen de la información disponible en Google Maps."
        )

        st.markdown("### ¿Encontraste un lugar que te gustó?")

        with st.form("form_guardar_lugar"):
            nombre_lugar = st.text_input(
                "Nombre del lugar",
                placeholder="Ej.: nombre de la cafetería",
            )

            zona_lugar = st.text_input(
                "Zona o dirección",
                value=busqueda["zona"],
            )

            guardar = st.form_submit_button(
                "♡ Guardar en favoritos",
                use_container_width=True,
            )

        if guardar:
            if not nombre_lugar.strip():
                st.warning("Escribí el nombre del lugar.")
            elif guardar_favorito(
                nombre_lugar,
                zona_lugar,
                busqueda["categoria"],
            ):
                st.success("¡Lugar guardado en tus favoritos!")
            else:
                st.info("Ese lugar ya está guardado.")

    st.markdown("---")
    st.markdown("### Inspirate con estas categorías")

    columnas = st.columns(2)

    for i, (categoria, descripcion) in enumerate(CATEGORIAS.items()):
        with columnas[i % 2]:
            with st.container(border=True):
                st.markdown(f"**{categoria}**")
                st.caption(descripcion.capitalize())

# =========================================================
# 10. CREAR UN PLAN
# =========================================================

with crear:
    st.markdown("## Creá una salida a tu manera")

    st.write(
        "Completá tus preferencias para organizar una salida "
        "con un presupuesto estimado y opciones alternativas."
    )

    with st.form("form_plan"):
        st.markdown("### 📍 Lugar y actividad")

        zona_plan = st.text_input(
            "Zona donde querés salir",
            placeholder="Ej.: Lanús, Buenos Aires",
        )

        actividad_plan = st.selectbox(
            "Tipo de salida",
            list(CATEGORIAS.keys()),
        )

        fecha_plan = st.date_input(
            "Fecha de la salida",
            value=date.today() + timedelta(days=1),
            min_value=date.today(),
        )

        hora_plan = st.selectbox(
            "Horario aproximado",
            ["Mañana", "Mediodía", "Tarde", "Atardecer", "Noche"],
        )

        st.markdown("### 👥 Grupo y presupuesto")

        personas_plan = st.number_input(
            "Cantidad de personas",
            min_value=1,
            max_value=100,
            value=2,
            step=1,
        )

        tipo_presupuesto = st.radio(
            "¿Cómo querés indicar el presupuesto?",
            ["Por persona", "Total del grupo"],
            horizontal=True,
        )

        presupuesto = st.number_input(
            "Presupuesto máximo en pesos ($)",
            min_value=0,
            value=10000,
            step=1000,
        )

        gasto_persona = st.number_input(
            "Gasto estimado por persona ($)",
            min_value=0,
            value=7000,
            step=500,
            help=(
                "Es una estimación editable, no un precio "
                "verificado de un lugar específico."
            ),
        )

        st.markdown("### 🚍 Transporte y preferencias")

        transporte = st.selectbox(
            "¿Cómo se van a trasladar?",
            TRANSPORTES,
        )

        preferencias = st.multiselect(
            "¿Qué tipo de ambiente prefieren?",
            PREFERENCIAS,
            default=["Económico"],
        )

        st.markdown("### 🌦️ Clima")

        ver_clima = st.checkbox(
            "Consultar el pronóstico para la fecha elegida",
            value=True,
        )

        enviar_plan = st.form_submit_button(
            "✨ Crear mi plan",
            type="primary",
            use_container_width=True,
        )

    if enviar_plan:
        if not zona_plan.strip():
            st.warning("Escribí una zona para organizar tu salida.")
        else:
            gasto_total = int(gasto_persona * personas_plan)

            if tipo_presupuesto == "Por persona":
                limite_total = presupuesto * personas_plan
            else:
                limite_total = presupuesto

            nuevo_plan = {
                "zona": zona_plan.strip(),
                "actividad": actividad_plan,
                "fecha": fecha_plan.isoformat(),
                "hora": hora_plan,
                "personas": int(personas_plan),
                "tipo_presupuesto": tipo_presupuesto,
                "presupuesto": int(presupuesto),
                "gasto_persona": int(gasto_persona),
                "gasto_total": gasto_total,
                "transporte": transporte,
                "preferencias": preferencias,
                "ver_clima": ver_clima,
            }

            st.session_state.planes.append(nuevo_plan)
            st.session_state.plan_actual = nuevo_plan

    plan = st.session_state.plan_actual

    if plan:
        st.markdown("---")
        st.markdown("## Tu plan está listo")

        st.markdown(
            f"### {plan['actividad']} en {plan['zona']}"
        )

        fecha_mostrar = date.fromisoformat(plan["fecha"]).strftime("%d/%m/%Y")

        st.write(
            f"**Fecha:** {fecha_mostrar}  \n"
            f"**Horario:** {plan['hora']}  \n"
            f"**Personas:** {plan['personas']}  \n"
            f"**Transporte:** {plan['transporte']}"
        )

        if plan["preferencias"]:
            st.write(
                "**Preferencias:** "
                + ", ".join(plan["preferencias"])
            )

        if plan["tipo_presupuesto"] == "Por persona":
            limite_total = plan["presupuesto"] * plan["personas"]
        else:
            limite_total = plan["presupuesto"]

        m1, m2, m3 = st.columns(3)

        m1.metric(
            "Costo por persona",
            dinero(plan["gasto_persona"]),
        )

        m2.metric(
            "Costo total estimado",
            dinero(plan["gasto_total"]),
        )

        m3.metric(
            "Presupuesto total",
            dinero(limite_total),
        )

        if plan["gasto_total"] <= limite_total:
            st.success("El gasto estimado está dentro del presupuesto.")
        else:
            st.warning(
                "El gasto estimado supera el presupuesto. "
                "Podés reducir el gasto por persona."
            )

        st.caption(
            "El costo es orientativo y no necesariamente incluye "
            "transporte, entradas ni gastos adicionales."
        )

        consulta_plan = (
            f"{CATEGORIAS[plan['actividad']]}, "
            f"{plan['zona']}, Argentina"
        )

        st.markdown("### 📍 Lugares y mapa")

        st.link_button(
            "Ver lugares para esta salida",
            buscar_maps(consulta_plan),
            use_container_width=True,
        )

        st.components.v1.iframe(
            "https://maps.google.com/maps?"
            + urlencode({
                "q": consulta_plan,
                "output": "embed",
            }),
            height=330,
            scrolling=False,
        )

        st.link_button(
            "Cómo llegar a la zona",
            crear_ruta(
                f"{plan['zona']}, Argentina",
                plan["transporte"],
            ),
            use_container_width=True,
        )

        if plan["ver_clima"]:
            st.markdown("### 🌤️ Pronóstico del tiempo")

            fecha_elegida = date.fromisoformat(plan["fecha"])
            dias = (fecha_elegida - date.today()).days

            if 0 <= dias <= 15:
                with st.spinner("Consultando el pronóstico..."):
                    clima = consultar_clima(
                        plan["zona"],
                        fecha_elegida,
                    )

                if clima and "error" not in clima:
                    cc1, cc2, cc3 = st.columns(3)

                    cc1.metric(
                        "Estado",
                        clima["emoji"] + " " + clima["descripcion"],
                    )

                    cc2.metric(
                        "Máxima",
                        f"{clima['max']} °C",
                    )

                    cc3.metric(
                        "Mínima",
                        f"{clima['min']} °C",
                    )

                    if clima["lluvia"] is not None:
                        st.write(
                            "**Probabilidad máxima de lluvia:** "
                            f"{clima['lluvia']}%"
                        )
                else:
                    st.info(
                        (clima or {}).get(
                            "error",
                            "No se pudo consultar el pronóstico.",
                        )
                    )
            else:
                st.info(
                    "El pronóstico se muestra para fechas cercanas, "
                    "cuando el servicio tiene datos disponibles."
                )

        st.markdown("### ☂️ Tu plan alternativo")

        if plan["actividad"] in [
            "Pasear",
            "Actividades al aire libre",
        ]:
            alternativa = (
                "cafeterías, cines y actividades bajo techo"
            )
            st.write(
                "Si llueve o hace mal tiempo, podés cambiar "
                "el paseo por una actividad bajo techo."
            )
        elif plan["actividad"] == "Ir al cine":
            alternativa = "cafeterías y actividades bajo techo"
            st.write(
                "Si el cine no está disponible, podés elegir "
                "una cafetería o una actividad alternativa."
            )
        else:
            alternativa = (
                f"{CATEGORIAS[plan['actividad']]} y "
                "otras actividades bajo techo"
            )
            st.write(
                "Si el lugar está cerrado o no se ajusta al "
                "presupuesto, buscá otra opción en la zona."
            )

        st.link_button(
            "Buscar el plan alternativo",
            buscar_maps(f"{alternativa}, {plan['zona']}, Argentina"),
            use_container_width=True,
        )

        st.markdown("### 💙 Guardar tu idea")

        if st.button(
            "♡ Guardar este plan en favoritos",
            use_container_width=True,
            key="guardar_plan",
        ):
            nombre_plan = (
                f"{plan['actividad']} en {plan['zona']}"
            )

            if guardar_favorito(
                nombre_plan,
                plan["zona"],
                plan["actividad"],
            ):
                st.success("¡Plan guardado en favoritos!")
            else:
                st.info("Este plan ya está guardado.")

# =========================================================
# 11. FAVORITOS E HISTORIAL
# =========================================================

with favoritos:
    st.markdown("## Tus favoritos 💙")

    st.write(
        "Acá encontrás los lugares y las ideas que guardaste."
    )

    if not st.session_state.favoritos:
        st.markdown("""
        <div class="section-card">
            <h3>Tu lista está esperando nuevas ideas</h3>
            <p>Entrá en «Explorar» y guardá los lugares que te gusten.</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.caption(
            f"{len(st.session_state.favoritos)} elemento(s) guardado(s)"
        )

        for i, favorito in enumerate(
            st.session_state.favoritos
        ):
            with st.container(border=True):
                info, accion = st.columns([3, 1])

                with info:
                    st.markdown(f"### {favorito['nombre']}")
                    st.caption(
                        f"{favorito['categoria']} · {favorito['zona']}"
                    )

                    st.link_button(
                        "📍 Ver en Google Maps",
                        favorito["url"],
                    )

                with accion:
                    if st.button(
                        "Quitar",
                        key=f"quitar_favorito_{i}",
                    ):
                        st.session_state.favoritos.pop(i)
                        st.rerun()

    st.markdown("---")
    st.markdown("## Historial de planes")

    if not st.session_state.planes:
        st.caption(
            "Todavía no creaste ningún plan. "
            "Podés hacerlo desde la pestaña correspondiente."
        )

    else:
        for i, plan_guardado in enumerate(
            reversed(st.session_state.planes)
        ):
            with st.container(border=True):
                st.markdown(
                    f"**{plan_guardado['actividad']} "
                    f"en {plan_guardado['zona']}**"
                )

                st.caption(
                    f"{plan_guardado['fecha']} · "
                    f"{plan_guardado['hora']} · "
                    f"{plan_guardado['personas']} persona(s)"
                )

                st.write(
                    "Costo total estimado: "
                    + dinero(plan_guardado["gasto_total"])
                )

                st.link_button(
                    "Ver zona en Maps",
                    buscar_maps(
                        f"{plan_guardado['zona']}, Argentina"
                    ),
                )

# =========================================================
# 12. PIE DE PÁGINA
# =========================================================

st.markdown("---")

st.markdown("""
<div style="text-align:center; padding:12px;">
    <p style="color:#64748B;">
        PLANLY · Encontrá tu próxima aventura 💙
    </p>
</div>
""", unsafe_allow_html=True)
