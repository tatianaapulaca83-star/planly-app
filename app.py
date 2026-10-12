
import streamlit as st
from pathlib import Path
from datetime import date, timedelta
from urllib.parse import urlencode, quote
from urllib.request import urlopen
from urllib.error import URLError
import json
import re
import base64
import uuid

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
    page_icon=str(icono) if icono.exists() else "P",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# 2. ESTILO VISUAL
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;500;600;700;800;900&display=swap');

:root {
    --azul: #4777D8;
    --azul-oscuro: #263F73;
    --celeste: #E8EEFF;
    --fondo: #F5F7FC;
    --texto: #263650;
    --suave: #64748B;
    --borde: #E0E6F3;
    --blanco: #FFFFFF;
}

.stApp {
    background: var(--fondo);
    color: var(--texto);
    font-family: 'Rockwell', 'Roboto Slab', serif;
}

h1, h2, h3, h4 {
    font-family: 'Rockwell', 'Roboto Slab', serif !important;
    color: var(--azul-oscuro);
    letter-spacing: -0.7px;
}

.hero h1 {
    font-family: 'Rockwell', 'Roboto Slab', serif !important;
    letter-spacing: 2px;
}

p, label, input, textarea, button, select, [data-testid="stMarkdownContainer"], [data-baseweb="select"] {
    font-family: 'Rockwell', 'Roboto Slab', serif !important;
}

.block-container {
    max-width: 1180px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

.hero {
    background: radial-gradient(circle at 88% 18%, rgba(214, 226, 255, .85), transparent 32%), linear-gradient(125deg, #E9EEFF 0%, #FFFFFF 58%, #F3F7FF 100%);
    border: 1px solid var(--borde);
    border-radius: 30px;
    padding: clamp(25px, 4.5vw, 44px);
    margin-bottom: 24px;
    box-shadow: 0 16px 42px rgba(42, 69, 126, 0.09);
}

.hero h1 {
    font-size: clamp(2.7rem, 6.5vw, 4.6rem);
    letter-spacing: 5px;
    font-weight: 800;
    margin: 0 0 10px 0;
    color: var(--azul-oscuro);
}

.hero p {
    color: #536783;
    font-size: 1.06rem;
    line-height: 1.75;
    margin: 5px 0 0 0;
}

.section-card {
    background: var(--blanco);
    border: 1px solid var(--borde);
    border-radius: 24px;
    padding: 25px;
    margin-bottom: 16px;
    box-shadow: 0 9px 28px rgba(35, 61, 112, 0.055);
}

.small-note {
    color: var(--suave);
    font-size: 0.88rem;
}

.optional-tag {
    display: inline-block;
    margin: 3px 0 5px 0;
    padding: 3px 8px;
    border-radius: 7px;
    background: #FFF0F0;
    color: #B42318;
    border: 1px solid #F6CACA;
    font-size: 0.68rem;
    font-weight: 900;
    letter-spacing: 0.7px;
}

/* Navegación elegante y adaptada a móvil */
div[data-testid="stTabs"] {
    margin-top: 8px;
}

div[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: rgba(232, 238, 255, .94);
    border: 1px solid #DCE4F5;
    border-radius: 18px;
    padding: 7px 9px;
    gap: 5px;
    box-shadow: 0 8px 22px rgba(37, 66, 125, 0.07);
}

div[data-testid="stTabs"] button {
    font-family: 'Rockwell', 'Roboto Slab', serif !important;
    font-size: 0.96rem;
    font-weight: 800;
    color: #536783;
    border-radius: 13px;
    padding: 11px 18px;
    border-bottom: 3px solid transparent;
    transition: background 0.18s ease, color 0.18s ease;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--azul);
    background: #FFFFFF;
    border-bottom-color: var(--azul);
}

div[data-testid="stTabs"] button:hover {
    color: var(--azul);
    background: rgba(255, 255, 255, 0.75);
}

div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    background: transparent;
}

/* Botones */
.stButton > button,
.stLinkButton > a,
.stFormSubmitButton > button {
    border-radius: 13px;
    font-family: 'Rockwell', 'Roboto Slab', serif !important;
    font-weight: 800;
    min-height: 48px;
    border: 1px solid #D5E2F8;
    transition: transform 0.16s ease, box-shadow 0.16s ease, background 0.16s ease;
}

.stButton > button:hover,
.stLinkButton > a:hover,
.stFormSubmitButton > button:hover {
    border-color: #8FB3F5;
    box-shadow: 0 5px 14px rgba(37, 99, 235, 0.10);
    transform: translateY(-1px);
}

.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background: #8FB7F5;
    border-color: #8FB7F5;
    color: #173B70;
}

.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover {
    background: #729FEA;
    border-color: #729FEA;
}

/* Campos y selectores */
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div,
div[data-baseweb="select"] > div {
    border-radius: 12px;
    border-color: #D7E2F3;
    background: #FFFFFF;
}

div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="textarea"] > div:focus-within,
div[data-baseweb="select"] > div:focus-within {
    border-color: #6D9EF0;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.10);
}

div[data-testid="stNumberInput"] button {
    border-radius: 9px;
    color: var(--azul);
}

div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid var(--borde);
    border-radius: 20px;
    padding: 17px 19px;
    box-shadow: 0 4px 15px rgba(23, 59, 122, 0.035);
}

div[data-testid="stAlert"] {
    border-radius: 14px;
}

div[data-testid="stExpander"] details {
    background: #FFFFFF;
    border: 1px solid var(--borde);
    border-radius: 14px;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--borde);
    border-radius: 17px;
}

img {
    border-radius: 16px;
}

iframe {
    border: 1px solid #DCE5F5 !important;
    border-radius: 20px !important;
    box-shadow: 0 10px 28px rgba(42, 69, 126, 0.10);
    overflow: hidden;
}

hr {
    border-color: var(--borde);
}

footer {
    visibility: hidden;
}

@media (max-width: 700px) {
    .block-container {
        padding-top: 0.8rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    div[data-testid="stTabs"] {
        position: sticky;
        bottom: 8px;
        z-index: 999;
        margin-top: 16px;
        padding-top: 8px;
        background: transparent;
    }

    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 2px;
        padding: 6px;
        border-radius: 20px;
        background: rgba(232, 238, 255, .97);
        box-shadow: 0 8px 28px rgba(35, 61, 112, .15);
        backdrop-filter: blur(12px);
    }

    div[data-testid="stTabs"] button {
        padding: 10px 5px;
        font-size: 0.78rem;
        min-height: 42px;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# PLAN COMPARTIDO (vista pública de solo lectura)
# =========================================================

try:
    codigo_plan_compartido = st.query_params.get("plan_compartido", "")
    plan_compartido = json.loads(
        base64.urlsafe_b64decode(codigo_plan_compartido.encode()).decode("utf-8")
    ) if codigo_plan_compartido else None
except (ValueError, TypeError, json.JSONDecodeError):
    plan_compartido = None

if plan_compartido:
    st.markdown("""
    <div class="hero">
        <p style="font-weight:800; letter-spacing:2px; text-transform:uppercase;">Un plan para compartir</p>
        <h1 style="font-size:clamp(2.2rem,5vw,3.4rem); letter-spacing:1px;">Planly</h1>
        <p>Te compartieron una salida. Acá tenés los detalles para organizarse.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"## {plan_compartido.get('actividad', 'Salida')}") 
    st.write(f"**Lugar:** {plan_compartido.get('lugar', '') or plan_compartido.get('zona', 'A definir')}")
    st.write(f"**Zona:** {plan_compartido.get('zona', 'A definir')}")
    st.write(f"**Fecha:** {plan_compartido.get('fecha_mostrar', 'A definir')}")
    st.write(f"**Hora de encuentro:** {plan_compartido.get('hora_exacta', 'A definir')}")
    st.write(f"**Horario de la salida:** {plan_compartido.get('hora', 'A definir')}")
    st.write(f"**Con quién:** {plan_compartido.get('con_quien', 'A definir')}")
    if plan_compartido.get("notas"):
        st.write(f"**Detalles:** {plan_compartido['notas']}")
    destino_compartido = plan_compartido.get('lugar') or plan_compartido.get('zona') or ''
    if destino_compartido:
        consulta_compartida = f"{plan_compartido.get('lugar')}, {plan_compartido.get('zona', '')}, Argentina" if plan_compartido.get('lugar') else f"{plan_compartido.get('zona', '')}, Argentina"
        st.link_button(
            "📍 Abrir el lugar en Google Maps",
            "https://www.google.com/maps/search/?" + urlencode({
                "api": "1",
                "query": consulta_compartida,
            }),
            use_container_width=True,
        )
    st.caption("Este enlace muestra una copia de los detalles compartidos. Los cambios posteriores del plan original no se actualizan automáticamente.")
    st.stop()

# =========================================================
# 2.1. AUTENTICACIÓN CON FIREBASE
# =========================================================

import requests
import extra_streamlit_components as stx

cookie_manager = stx.CookieManager(key='planly_auth_cookies')

FIREBASE_API_KEY = st.secrets["firebase"]["api_key"]
FIREBASE_PROJECT_ID = st.secrets["firebase"]["project_id"]

URL_AUTH = (
    "https://identitytoolkit.googleapis.com/v1/accounts"
)


def renovar_sesion_firebase(refresh_token):
    try:
        respuesta = requests.post(
            "https://securetoken.googleapis.com/v1/token",
            params={"key": FIREBASE_API_KEY},
            data={"grant_type": "refresh_token", "refresh_token": refresh_token},
            timeout=15,
        )
        datos = respuesta.json()
        if not respuesta.ok:
            return None
        return {
            "uid": datos.get("user_id"),
            "email": datos.get("email"),
            "id_token": datos.get("id_token"),
            "refresh_token": datos.get("refresh_token", refresh_token),
        }
    except (requests.RequestException, ValueError):
        return None


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
    token_guardado = cookie_manager.get("planly_refresh_token")
    if token_guardado:
        usuario_recuperado = renovar_sesion_firebase(token_guardado)
        if usuario_recuperado and usuario_recuperado.get("uid"):
            st.session_state.firebase_user = usuario_recuperado
            cookie_manager.set("planly_refresh_token", usuario_recuperado["refresh_token"], key="actualizar_sesion_planly")

if not st.session_state.firebase_user:
    acceso_texto, acceso_momi = st.columns([1.35, 1], gap="large", vertical_alignment="center")
    with acceso_texto:
        st.markdown("""
        <div class="hero">
            <p style="font-weight:800; letter-spacing:2px; text-transform:uppercase;">Tu próxima historia empieza acá</p>
            <h1 style="font-size:clamp(2.2rem,5vw,3.4rem); letter-spacing:1px;">Planly</h1>
            <p>Organizá salidas, descubrí lugares y guardá tus ideas favoritas.</p>
        </div>
        """, unsafe_allow_html=True)
    with acceso_momi:
        pose_acceso = CARPETA / IMAGENES_EXTRA[1]
        if pose_acceso.exists():
            st.image(str(pose_acceso), use_container_width=True)
        elif (CARPETA / MOMI).exists():
            st.image(str(CARPETA / MOMI), use_container_width=True)

    st.markdown("## Bienvenido/a")
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
            recordar_sesion = st.checkbox(
                "Mantener mi sesión iniciada en este dispositivo",
                value=True,
                help="Activá esta opción solo en un dispositivo personal.",
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
                    if recordar_sesion:
                        cookie_manager.set("planly_refresh_token", st.session_state.firebase_user["refresh_token"], key="guardar_sesion_planly")
                    else:
                        cookie_manager.delete("planly_refresh_token", key="borrar_sesion_planly")
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

with st.sidebar:
    st.caption(f"Sesión iniciada: {st.session_state.firebase_user.get('email', 'tu cuenta')}")
    if st.button("Cerrar sesión", use_container_width=True):
        st.session_state.firebase_user = None
        cookie_manager.delete("planly_refresh_token", key="cerrar_sesion_planly")
        st.session_state.firestore_cargado = False
        st.session_state.planes = []
        st.session_state.favoritos = []
        st.rerun()

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


def mostrar_momi(indice=0, ancho=None):
    """Muestra una pose de Momi para acompañar cada sección."""
    poses = [nombre for nombre in IMAGENES_EXTRA if archivo(nombre).exists()]
    imagen = archivo(poses[indice % len(poses)]) if poses else archivo(MOMI)
    if imagen.exists():
        st.image(str(imagen), use_container_width=True)

def buscar_maps(consulta):
    parametros = urlencode({
        "api": "1",
        "query": consulta,
    })
    return "https://www.google.com/maps/search/?" + parametros

def url_maps_plan(plan):
    """Prioriza el lugar exacto escrito por la persona; si falta, usa la zona."""
    destino = (plan.get("lugar") or "").strip()
    zona = (plan.get("zona") or "").strip()
    consulta = f"{destino}, {zona}, Argentina" if destino else f"{zona}, Argentina"
    return buscar_maps(consulta)


@st.dialog("Detalles de tu plan", width="large")
def mostrar_detalle_plan_guardado(plan, clave):
    """Abre los detalles del plan en una ventana emergente, no al fondo de la página."""
    st.markdown("### Detalles de tu plan")
    st.markdown(f"#### {plan.get('actividad', 'Salida')} en {plan.get('zona', 'Zona a definir')}")
    fecha = plan.get("fecha", "")
    try:
        fecha = date.fromisoformat(fecha).strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        fecha = fecha or "A definir"

    st.write(f"**Lugar exacto:** {plan.get('lugar') or 'Todavía por decidir'}")
    st.write(f"**Zona:** {plan.get('zona') or 'A definir'}")
    st.write(f"**Fecha:** {fecha}")
    st.write(f"**Hora de encuentro:** {plan.get('hora_exacta', 'A definir')}")
    st.write(f"**Horario de la salida:** {plan.get('hora', 'A definir')}")
    st.write(f"**Con quién:** {plan.get('con_quien') or 'Todavía por decidir'}")
    st.write(f"**Cantidad de personas:** {plan.get('personas', 'A definir')}")
    st.write(f"**Transporte:** {plan.get('transporte', 'A definir')}")
    st.write(f"**Presupuesto:** {dinero(plan.get('presupuesto', 0))} ({plan.get('tipo_presupuesto', 'No especificado')})")
    st.write(f"**Gasto estimado por persona:** {dinero(plan.get('gasto_persona', 0))}")
    st.write(f"**Gasto total estimado:** {dinero(plan.get('gasto_total', 0))}")
    preferencias = plan.get("preferencias", [])
    if preferencias:
        st.write("**Preferencias:** " + ", ".join(preferencias))
    if plan.get("notas"):
        st.write(f"**Notas:** {plan['notas']}")

    st.link_button(
        "📍 Ver este lugar en Google Maps",
        url_maps_plan(plan),
        use_container_width=True,
    )
    st.link_button(
        "Cómo llegar",
        crear_ruta(
            f"{(plan.get('lugar') or plan.get('zona') or '').strip()}, Argentina",
            plan.get("transporte", "Todavía no lo sé"),
        ),
        use_container_width=True,
    )
    if st.button("Cerrar detalles", key=f"cerrar_detalle_{clave}", use_container_width=True):
        st.session_state.plan_seleccionado_guardado = None
        st.rerun()

@st.dialog("Eliminar plan", width="small")
def confirmar_eliminar_plan(indice):
    """Pide confirmación antes de borrar un plan guardado."""
    if not isinstance(indice, int) or not (0 <= indice < len(st.session_state.planes)):
        st.session_state.plan_pendiente_eliminar = None
        st.rerun()

    plan = st.session_state.planes[indice]
    st.write(f"¿Querés eliminar **{plan.get('actividad', 'este plan')}** de tus planes guardados?")
    st.caption("Esta acción no se puede deshacer.")

    col_borrar, col_cancelar = st.columns(2)
    with col_borrar:
        if st.button("Sí, eliminar", type="primary", key="confirmar_borrado_plan", use_container_width=True):
            planes_anteriores = list(st.session_state.planes)
            st.session_state.planes.pop(indice)
            try:
                guardar_datos_firestore(st.session_state.planes, st.session_state.favoritos)
                st.session_state.plan_pendiente_eliminar = None
                seleccionado = st.session_state.get("plan_seleccionado_guardado")
                if seleccionado == indice:
                    st.session_state.plan_seleccionado_guardado = None
                elif isinstance(seleccionado, int) and seleccionado > indice:
                    st.session_state.plan_seleccionado_guardado = seleccionado - 1
                st.session_state.aviso_plan_eliminado = True
                st.rerun()
            except Exception:
                st.session_state.planes = planes_anteriores
                st.error("No pudimos guardar el cambio. El plan sigue en tu historial; revisá la conexión e intentá otra vez.")
    with col_cancelar:
        if st.button("Cancelar", key="cancelar_borrado_plan", use_container_width=True):
            st.session_state.plan_pendiente_eliminar = None
            st.rerun()


def clave_orden_archivo(ruta):
    """Ordena nombres como foto2 antes que foto10, aunque mezclen números y letras."""
    return [(0, int(parte)) if parte.isdigit() else (1, parte.casefold())
            for parte in re.split(r"(\d+)", ruta.name)]


def imagenes_locales_turisticos():
    """Devuelve las fotos del repositorio para asociarlas por nombre, no por orden."""
    extensiones = {".jpg", ".jpeg", ".png", ".webp"}
    nombres_de_momi = {MOMI, FAVICON, VIDEO, *IMAGENES_EXTRA}
    carpeta_fotos = CARPETA / "imagenes_lugares"
    candidatos = []

    if carpeta_fotos.exists():
        candidatos.extend(
            p for p in carpeta_fotos.iterdir()
            if p.is_file() and p.suffix.lower() in extensiones
        )

    candidatos.extend(
        p for p in CARPETA.iterdir()
        if p.is_file()
        and p.suffix.lower() in extensiones
        and p.name not in nombres_de_momi
        and p not in candidatos
    )
    return candidatos


def obtener_foto_turistica(titulo, indice=None):
    """Usa una foto local solo si el nombre identifica el lugar; si no, busca su foto propia."""
    fotos = imagenes_locales_turisticos()
    nombre = titulo.casefold()

    # Asociaciones explícitas: nunca se asignan fotos según el orden alfabético.
    palabras_clave = {
        "parque de la costa": ("parque-de-la-costa",),
        "puerto de frutos": ("puerto-de-frutos", "puerto_de_frutos"),
        "museo de arte tigre": ("mat-tigre", "museo-de-arte-tigre"),
        "caminito": ("caminito",),
        "obelisco": ("obelisco",),
        "planetario": ("planetario",),
        "reserva ecológica": ("reserva-ecologica", "reserva_ecologica", "costanera-sur"),
        "temaikèn": ("temaiken", "temaikén"),
        "temaiken": ("temaiken", "temaikén"),
    }

    claves = next((v for k, v in palabras_clave.items() if k in nombre), ())
    for foto in fotos:
        nombre_archivo = foto.name.casefold()
        if any(clave in nombre_archivo for clave in claves):
            return str(foto)

    # Si no existe una imagen local identificable para ese lugar, usar su propia foto de Wikipedia.
    try:
        url = "https://es.wikipedia.org/api/rest_v1/page/summary/" + quote(titulo.replace(" ", "_"), safe="")
        respuesta = requests.get(url, timeout=6)
        if respuesta.ok:
            datos = respuesta.json()
            miniatura = datos.get("thumbnail", {}).get("source")
            if miniatura:
                return miniatura
    except (requests.RequestException, ValueError):
        pass
    return None


def crear_ruta(destino, transporte, origen=None):
    modos = {
        "Caminando": "walking",
        "Colectivo": "transit",
        "Tren": "transit",
        "Auto": "driving",
        "Transporte por aplicación": "driving",
        "Todavía no lo sé": "transit",
    }

    parametros = {
        "api": "1",
        "destination": destino,
        "travelmode": modos.get(transporte, "transit"),
    }
    if origen:
        parametros["origin"] = origen
    return "https://www.google.com/maps/dir/?" + urlencode(parametros)


def buscar_alrededor(consulta, zona):
    return buscar_maps(f"{consulta} cerca de {zona}, Argentina")


def buscar_info_lugar(nombre):
    return "https://www.google.com/search?" + urlencode({
        "q": f"{nombre} entrada precio horarios sitio oficial"
    })

def dinero(valor):
    return "$"+ f"{valor:,.0f}".replace(",", ".")

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

    try:
        guardar_datos_firestore(
            st.session_state.planes,
            st.session_state.favoritos,
        )
    except Exception:
        st.warning(
            "El favorito quedó en esta sesión, pero no pudimos sincronizarlo "
            "con tu cuenta. Revisá tu conexión e intentá nuevamente."
        )

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
            0: ("Despejado", ""),
            1: ("Mayormente despejado", ""),
            2: ("Parcialmente nublado", ""),
            3: ("Nublado", ""),
            45: ("Niebla", ""),
            48: ("Niebla", ""),
            51: ("Llovizna leve", ""),
            53: ("Llovizna", ""),
            55: ("Llovizna intensa", ""),
            61: ("Lluvia leve", ""),
            63: ("Lluvia", ""),
            65: ("Lluvia intensa", ""),
            71: ("Nieve leve", ""),
            73: ("Nieve", ""),
            75: ("Nieve intensa", ""),
            80: ("Chaparrones leves", ""),
            81: ("Chaparrones", ""),
            82: ("Chaparrones intensos", ""),
            95: ("Tormenta", ""),
            96: ("Tormenta con granizo", ""),
            99: ("Tormenta intensa", ""),
        }

        descripcion, emoji = descripciones.get(
            codigo, ("Estado variable", "")
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

if "plan_seleccionado_guardado" not in st.session_state:
    st.session_state.plan_seleccionado_guardado = None
    
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
    <p style="font-weight:800; letter-spacing:1px;">ENCONTRÁ TU PRÓXIMO LUGAR FAVORITO</p>
    <p>Ideas para salir, compartir y disfrutar a tu manera.</p>
</div>
""", unsafe_allow_html=True)
if archivo(VIDEO).exists():
    st.video(str(archivo(VIDEO)))

# =========================================================
# 7. PESTAÑAS
# =========================================================

inicio, explorar, crear, favoritos = st.tabs([
    "Inicio",
    "Explorar",
    "Crear un plan",
    "Favoritos",
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
            <p> Descubrir cafeterías y meriendas</p>
            <p> Encontrar heladerías</p>
            <p> Conocer parques y paseos</p>
            <p> Buscar actividades para compartir</p>
            <p> Organizar gastos y alternativas</p>
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
            st.markdown("## ¡Hola! Soy MOMI ")
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

    st.caption("El video de presentación está disponible en el encabezado de Planly.")

    st.markdown("---")
    st.markdown("### Tus planes guardados")
    if not st.session_state.planes:
        st.caption("Cuando crees y guardes un plan, lo vas a encontrar acá.")
    else:
        for indice_inicio, plan_inicio in list(enumerate(reversed(st.session_state.planes)))[:3]:
            indice_real_inicio = len(st.session_state.planes) - 1 - indice_inicio
            with st.container(border=True):
                st.markdown(f"**{plan_inicio.get('actividad', 'Salida')} · {plan_inicio.get('lugar') or plan_inicio.get('zona', 'Lugar a definir')}**")
                st.caption(f"{plan_inicio.get('fecha', 'Fecha a definir')} · {plan_inicio.get('hora', 'Horario a definir')} · {plan_inicio.get('personas', '?')} persona(s)")
                ver_col, mapa_col, borrar_col = st.columns([1, 1, 0.8])
                with ver_col:
                    if st.button("Ver detalles", key=f"inicio_detalle_{indice_real_inicio}", use_container_width=True):
                        st.session_state.plan_seleccionado_guardado = indice_real_inicio
                with mapa_col:
                    st.link_button("Ver en el mapa", url_maps_plan(plan_inicio), use_container_width=True)
                with borrar_col:
                    if st.button("🗑️ Eliminar", key=f"inicio_eliminar_{indice_real_inicio}", use_container_width=True):
                        st.session_state.plan_pendiente_eliminar = indice_real_inicio



# =========================================================
# 9. EXPLORAR
# =========================================================

with explorar:
    intro_explorar, momi_explorar = st.columns([1.7, 1], gap="large", vertical_alignment="center")
    with intro_explorar:
        st.markdown("## Explorá lugares")
        st.write("Encontrá un rincón nuevo para merendar, pasear o compartir algo lindo.")
    with momi_explorar:
        mostrar_momi(2)
    st.markdown("### ¿Qué te gustaría descubrir?")

    with st.form("form_explorar"):
        zona_explorar = st.text_input(
            "¿En qué zona querés buscar?",
            placeholder="Ej.: Lanús, Banfield, Lomas de Zamora",
        )

        categoria_explorar = st.selectbox(
            "¿Qué te gustaría hacer?",
            list(CATEGORIAS.keys()),
        )

        presupuesto_explorar = st.selectbox(
            "¿Qué presupuesto tenés en mente?",
            [
                "Cualquier presupuesto",
                "Gratis o muy económico",
                "Económico",
                "Intermedio",
            ],
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
                "presupuesto": presupuesto_explorar,
                "consulta": (
                    f"{CATEGORIAS[categoria_explorar]}, "
                    + (
                        "gratis o económico, "
                        if presupuesto_explorar == "Gratis o muy económico"
                        else "económico, "
                        if presupuesto_explorar == "Económico"
                        else "precio moderado, "
                        if presupuesto_explorar == "Intermedio"
                        else ""
                    )
                    + f"{zona_explorar.strip()}, Argentina"
                ),
            }

    busqueda = st.session_state.busqueda_actual

    if busqueda:
        st.markdown("### Opciones para descubrir")

        st.write(
            f"Buscando **{busqueda['categoria'].lower()}** en "
            f"**{busqueda['zona']}**."
        )
        if busqueda.get("presupuesto", "Cualquier presupuesto") != "Cualquier presupuesto":
            st.caption(
                f"Preferencia de presupuesto: {busqueda['presupuesto']}. "
                "Es una orientación para la búsqueda; verificá los precios con cada lugar."
            )

        st.link_button(
            "Ver resultados en Google Maps",
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
                "Guardar en favoritos",
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
    st.markdown("## Lugares turísticos para conocer")
    st.write("Ideas de paseos reales por Buenos Aires y alrededores. Abrí el mapa para revisar horarios, entradas y cómo llegar.")

    lugares_turisticos = [
        {
            "nombre": "Parque de la Costa",
            "wiki": "Parque de la Costa",
            "zona": "Tigre, Buenos Aires",
            "descripcion": "Parque de diversiones con juegos y atracciones para pasar varias horas.",
            "costo": "Entrada paga. El valor depende del tipo de pase y la fecha.",
            "busqueda": "Parque de la Costa, Tigre, Buenos Aires",
        },
        {
            "nombre": "Puerto de Frutos",
            "wiki": "Puerto de Frutos",
            "zona": "Tigre, Buenos Aires",
            "descripcion": "Paseo junto al río con puestos, artesanías, decoración y opciones para comer.",
            "costo": "Recorrerlo es gratis; compras y consumos se pagan aparte.",
            "busqueda": "Puerto de Frutos, Tigre, Buenos Aires",
        },
        {
            "nombre": "Museo de Arte Tigre",
            "wiki": "Museo de Arte Tigre",
            "zona": "Tigre, Buenos Aires",
            "descripcion": "Museo en un edificio histórico frente al río, con exposiciones de arte.",
            "costo": "La entrada y los descuentos pueden variar; confirmar antes de ir.",
            "busqueda": "Museo de Arte Tigre, Buenos Aires",
        },
        {
            "nombre": "Caminito",
            "wiki": "Caminito",
            "zona": "La Boca, Ciudad de Buenos Aires",
            "descripcion": "Calle museo al aire libre, conocida por sus casas coloridas, artistas y tango.",
            "costo": "Recorrer la calle es gratis; comer o comprar recuerdos tiene costo.",
            "busqueda": "Caminito, La Boca, Buenos Aires",
        },
        {
            "nombre": "Obelisco",
            "wiki": "Obelisco de Buenos Aires",
            "zona": "Centro, Ciudad de Buenos Aires",
            "descripcion": "Monumento emblemático de la ciudad, ideal para una parada breve y fotos.",
            "costo": "Verlo desde el espacio público es gratis.",
            "busqueda": "Obelisco de Buenos Aires",
        },
        {
            "nombre": "Planetario Galileo Galilei",
            "wiki": "Planetario Galileo Galilei",
            "zona": "Palermo, Ciudad de Buenos Aires",
            "descripcion": "Un paseo para aprender sobre astronomía mediante funciones y actividades.",
            "costo": "Las funciones pueden ser pagas; consultar la programación y tarifa vigente.",
            "busqueda": "Planetario Galileo Galilei, Buenos Aires",
        },
        {
            "nombre": "Reserva Ecológica Costanera Sur",
            "wiki": "Reserva Ecológica de Buenos Aires",
            "zona": "Puerto Madero, Ciudad de Buenos Aires",
            "descripcion": "Senderos para caminar, observar aves y disfrutar de la naturaleza al aire libre.",
            "costo": "El acceso general suele ser gratuito; revisar avisos por cierres o actividades.",
            "busqueda": "Reserva Ecológica Costanera Sur, Buenos Aires",
        },
        {
            "nombre": "Temaikèn",
            "wiki": "Temaikèn",
            "zona": "Belén de Escobar, Buenos Aires",
            "descripcion": "Bioparque con animales, ambientes naturales y espacios educativos para recorrer en familia.",
            "costo": "Entrada paga; consultar el precio vigente y comprar solo en canales oficiales.",
            "busqueda": "Temaikèn, Escobar, Buenos Aires",
        },
    ]

    tonos_lugares = [
        ("#EAF1FF", "#4269B2", "#D4E2FF"),
        ("#E4F5FF", "#28749A", "#C6E9FA"),
        ("#F0EBFF", "#7055A5", "#DDD2FF"),
        ("#E8F0FF", "#4965A0", "#D2DFFF"),
    ]

    for inicio_lote in range(0, len(lugares_turisticos), 2):
        columnas_lugares = st.columns(2, gap="large")
        for columna, lugar in zip(columnas_lugares, lugares_turisticos[inicio_lote:inicio_lote + 2]):
            with columna:
                fondo_lugar, texto_lugar, borde_lugar = tonos_lugares[(inicio_lote // 2) % len(tonos_lugares)]
                with st.container(border=True):
                    foto_lugar = obtener_foto_turistica(lugar["wiki"], lugares_turisticos.index(lugar))
                    if foto_lugar:
                        st.image(foto_lugar, use_container_width=True)
                    else:
                        st.markdown(
                            f'<div style="background:{fondo_lugar}; border:1px dashed {borde_lugar}; border-radius:14px; padding:24px; color:{texto_lugar}; text-align:center; font-weight:700;">Foto no disponible por el momento</div>',
                            unsafe_allow_html=True,
                        )
                    st.markdown(f"### {lugar['nombre']}")
                    st.caption(lugar["zona"])
                    st.write(lugar["descripcion"])
                    st.caption("**Costo orientativo:** " + lugar["costo"])
                    st.link_button(
                        "Consultar precio y horarios",
                        buscar_info_lugar(lugar["nombre"]),
                        use_container_width=True,
                    )
                    st.link_button(
                        "Ver en Google Maps",
                        buscar_maps(lugar["busqueda"]),
                        use_container_width=True,
                    )

    st.caption("Planly usa primero las fotos que subiste al repositorio; si no encuentra una, intenta mostrar una imagen de Wikipedia. Los precios pueden cambiar: confirmalos antes de salir.")

# =========================================================
# 10. CREAR UN PLAN
# =========================================================

with crear:
    intro_plan, momi_plan = st.columns([1.65, 1], gap="large", vertical_alignment="center")
    with intro_plan:
        st.markdown("## Armemos algo lindo")
        st.write("Contale a Planly qué tenés ganas de hacer. Momi te acompaña a organizar la salida, el presupuesto y un plan alternativo.")
    with momi_plan:
        mostrar_momi(5)

    with st.form("form_plan"):
        st.markdown("### Empecemos por la idea")

        zona_plan = st.text_input(
            "Zona donde querés salir",
            placeholder="Ej.: Lanús, Buenos Aires",
        )

        st.markdown("### ¿Ya elegiste el lugar? Anotalo acá")
        lugar_especifico_plan = st.text_input(
            "Nombre exacto del lugar (como aparece en Google Maps)",
            placeholder="Ej.: MP3 Karaoke, Lanús",
            help="Buscá el lugar en Google Maps, copiá su nombre y pegalo acá. Planly no puede detectar automáticamente qué lugar tocaste en Google Maps.",
        )
        st.caption("Si todavía no lo decidiste, podés dejarlo vacío y agregarlo después de crear el plan.")

        actividad_plan = st.selectbox(
            "Tipo de salida",
            list(CATEGORIAS.keys()),
        )

        st.markdown('<span class="optional-tag">OPCIONAL · SOLO SI ELEGISTE «OTRA ACTIVIDAD»</span>', unsafe_allow_html=True)
        detalle_actividad_plan = st.text_input(
            "Si elegiste «Otra actividad», ¿qué querés hacer?",
            placeholder="Ej.: jugar al bowling, escalar en palestra, andar en bici, hacer kayak",
            help="Si elegís otra actividad, escribila acá para buscar lugares más precisos.",
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

        hora_exacta_plan = st.selectbox(
            "¿A qué hora se encuentran?",
            [f"{h:02d}:{m:02d}" for h in range(7, 24) for m in (0, 15, 30, 45)],
            index=32,
        )

        st.markdown('<span class="optional-tag">OPCIONAL</span>', unsafe_allow_html=True)
        con_quien_plan = st.text_input(
            "¿Con quién vas?",
            placeholder="Ej.: con mi amiga, con mi familia o con compañeros",
        )

        st.markdown('<span class="optional-tag">OPCIONAL</span>', unsafe_allow_html=True)
        notas_plan = st.text_area(
            "Detalles para acordarse",
            placeholder="Ej.: nos encontramos en la entrada, llevar SUBE, comprar entradas antes...",
            height=90,
        )

        st.markdown("### Tu grupo y tu presupuesto")

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

        st.markdown("### Cómo quieren salir")

        transporte = st.selectbox(
            "¿Cómo se van a trasladar?",
            TRANSPORTES,
        )

        preferencias = st.multiselect(
            "¿Qué tipo de ambiente prefieren?",
            PREFERENCIAS,
            default=["Económico"],
        )

        st.markdown("### Revisemos el clima")

        ver_clima = st.checkbox(
            "Consultar el pronóstico para la fecha elegida",
            value=True,
        )

        enviar_plan = st.form_submit_button(
            "Crear mi plan",
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

            actividad_final = (
                detalle_actividad_plan.strip()
                if actividad_plan == "Otra actividad" and detalle_actividad_plan.strip()
                else actividad_plan
            )

            nuevo_plan = {
                "id": uuid.uuid4().hex,
                "zona": zona_plan.strip(),
                "lugar": lugar_especifico_plan.strip(),
                "hora_exacta": hora_exacta_plan,
                "con_quien": con_quien_plan.strip(),
                "notas": notas_plan.strip(),
                "actividad": actividad_final,
                "categoria_original": actividad_plan,
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
            st.session_state["lugar_editar_plan_actual"] = nuevo_plan["lugar"]

            try:
                guardar_datos_firestore(
                    st.session_state.planes,
                    st.session_state.favoritos,
                )
            except Exception:
                st.warning(
                    "El plan se creó, pero no pudimos guardarlo "
                    "en tu cuenta. Revisá tu conexión e intentá nuevamente."
                )

    plan = st.session_state.plan_actual

    if plan:
        st.markdown("---")
        st.markdown("## Tu plan está listo")


        st.markdown(
            f"### {plan['actividad']} en {plan['zona']}"
        )

        fecha_mostrar = date.fromisoformat(plan["fecha"]).strftime("%d/%m/%Y")

        st.write(
            f"**Lugar específico:** {plan.get('lugar') or 'Todavía por decidir'}  \n"
            f"**Fecha:** {fecha_mostrar}  \n"
            f"**Hora de encuentro:** {plan.get('hora_exacta', 'A definir')}  \n"
            f"**Horario:** {plan['hora']}  \n"
            f"**Con quién:** {plan.get('con_quien') or 'Todavía por decidir'}  \n"
            f"**Personas:** {plan['personas']}  \n"
            f"**Transporte:** {plan['transporte']}"
        )
        if plan.get("notas"):
            st.write(f"**Detalles:** {plan['notas']}")

        st.markdown("### ¿Elegiste otro lugar o querés confirmar el destino?")
        st.caption("Podés buscarlo en Google Maps y después escribir acá el nombre exacto. Al guardar, también se actualizará el plan que tenés guardado.")
        with st.form("actualizar_destino_plan"):
            nuevo_destino_plan = st.text_input(
                "Lugar exacto",
                key="lugar_editar_plan_actual",
                placeholder="Ej.: MP3 Karaoke, Lanús",
            )
            guardar_destino_plan = st.form_submit_button(
                "Guardar lugar en mi plan",
                use_container_width=True,
            )

        if guardar_destino_plan:
            plan["lugar"] = nuevo_destino_plan.strip()
            plan_id_actual = plan.get("id")
            plan_actualizado = False
            for plan_guardado in st.session_state.planes:
                if (
                    (plan_id_actual and plan_guardado.get("id") == plan_id_actual)
                    or plan_guardado is plan
                ):
                    plan_guardado["lugar"] = nuevo_destino_plan.strip()
                    plan_actualizado = True
                    break
            if plan_actualizado:
                try:
                    guardar_datos_firestore(
                        st.session_state.planes,
                        st.session_state.favoritos,
                    )
                    st.success(
                        f"Lugar guardado: {nuevo_destino_plan.strip()}"
                        if nuevo_destino_plan.strip()
                        else "Se quitó el lugar específico de este plan."
                    )
                except Exception:
                    st.error("No pudimos sincronizar el cambio con tu cuenta. Intentá nuevamente.")
            else:
                st.warning("No encontramos este plan en tu historial para guardar el cambio.")
            st.rerun()

        if plan["preferencias"]:
            st.write(
                "**Preferencias:** "
                + ", ".join(plan["preferencias"])
            )

        # Mostrar el mapa inmediatamente debajo de los datos principales del plan.
        destino_especifico = plan.get("lugar", "").strip()
        if plan.get("categoria_original") == "Otra actividad":
            actividad_busqueda = plan["actividad"]
        else:
            actividad_busqueda = CATEGORIAS.get(
                plan.get("categoria_original", plan["actividad"]),
                plan["actividad"],
            )
        preferencias_mapa = [
            preferencia.lower()
            for preferencia in plan["preferencias"]
            if preferencia != "Indistinto"
        ]
        detalle_mapa = (
            ", " + ", ".join(preferencias_mapa)
            if preferencias_mapa
            else ""
        )
        consulta_plan = (
            f"{destino_especifico}, {plan['zona']}, Argentina"
            if destino_especifico
            else f"{actividad_busqueda}{detalle_mapa}, {plan['zona']}, Argentina"
        )

        st.markdown("### Lugares y mapa")
        st.caption(f"Buscamos opciones relacionadas con: {plan['actividad']}")

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

        st.markdown("### Tu plan del día")
        st.write("Este es un horario orientativo que podés adaptar según los turnos, el viaje y el presupuesto.")

        agenda = {
            "Mañana": [("09:30", "Llegada y traslado"), ("10:00–12:00", "Actividad principal"), ("12:15", "Pausa para comer"), ("13:30", "Paseo corto o descanso"), ("15:00", "Regreso según el transporte disponible")],
            "Mediodía": [("12:00", "Llegada y traslado"), ("12:30–14:00", "Actividad principal"), ("14:15", "Pausa para comer"), ("15:30", "Paseo corto o descanso"), ("17:00", "Regreso según el transporte disponible")],
            "Tarde": [("15:00", "Llegada y traslado"), ("15:30–17:30", "Actividad principal"), ("17:45", "Merienda o pausa"), ("18:30", "Paseo corto o descanso"), ("20:00", "Regreso según el transporte disponible")],
            "Atardecer": [("17:00", "Llegada y traslado"), ("17:30–19:00", "Actividad principal"), ("19:15", "Pausa para comer"), ("20:15", "Paseo corto o descanso"), ("21:00", "Regreso según el transporte disponible")],
            "Noche": [("19:00", "Llegada y traslado"), ("19:30–21:00", "Actividad principal"), ("21:15", "Cena o algo para comer"), ("22:00", "Preparar el regreso"), ("22:30", "Volver según el transporte disponible")],
        }
        for horario, titulo in agenda.get(plan["hora"], agenda["Tarde"]):
            with st.container(border=True):
                st.markdown(f"**{horario} · {titulo}**")
                if titulo == "Actividad principal":
                    st.write(f"Tiempo sugerido para disfrutar: {plan['actividad']}. Revisá si necesitás entrada o reserva.")
                elif titulo == "Pausa para comer" or titulo == "Merienda o pausa" or titulo == "Cena o algo para comer":
                    if plan["gasto_total"] > limite_total:
                        st.write("Para cuidar el presupuesto, buscá una opción económica o llevá algo preparado.")
                    else:
                        st.write("Elegí un lugar cercano que encaje con el presupuesto y revisá los precios del menú.")
                elif titulo == "Paseo corto o descanso":
                    st.write("Si queda tiempo, sumá una caminata o un lugar gratuito cercano; si no, disfrutá sin apuro.")
                elif titulo == "Llegada y traslado":
                    st.write(f"Organizá el viaje hacia {plan['zona']} y revisá posibles demoras en Google Maps.")
                else:
                    st.write("Consultá el recorrido actualizado antes de salir para calcular el tiempo de viaje.")

        st.link_button(
            "Buscar dónde comer cerca",
            buscar_alrededor("restaurantes económicos", plan["zona"]),
            use_container_width=True,
        )

        st.markdown("### Opciones cerca de tu salida")
        st.write("Además del mapa, podés abrir búsquedas específicas de lugares cercanos. Google Maps mostrará las opciones disponibles según la zona.")
        categorias_cercanas = [
            ("Restaurantes", "restaurantes"),
            ("Cafeterías y meriendas", "cafeterías para merendar"),
            ("Heladerías", "heladerías"),
            ("Parques y paseos", "parques y lugares para pasear"),
        ]
        columnas_cercanas = st.columns(2, gap="medium")
        for i, (etiqueta_cercana, consulta_cercana) in enumerate(categorias_cercanas):
            with columnas_cercanas[i % 2]:
                st.link_button(
                    etiqueta_cercana,
                    buscar_alrededor(consulta_cercana, plan["zona"]),
                    use_container_width=True,
                )

        st.markdown("### Cómo llegar y cuánto tarda")
        st.write(
            "Elegí el medio de transporte y Google Maps calculará el recorrido y los minutos "
            "estimados con el tránsito y los servicios disponibles en ese momento. Planly no inventa tiempos de viaje."
        )
        destino_ruta = consulta_plan
        origen_ruta = f"{plan['zona']}, Argentina"
        col_ruta1, col_ruta2 = st.columns(2, gap="medium")
        with col_ruta1:
            st.link_button(
                "Ruta en transporte público",
                crear_ruta(destino_ruta, "Colectivo", origen=origen_ruta),
                use_container_width=True,
            )
            st.link_button(
                "Ruta caminando",
                crear_ruta(destino_ruta, "Caminando", origen=origen_ruta),
                use_container_width=True,
            )
        with col_ruta2:
            st.link_button(
                "Ruta en auto",
                crear_ruta(destino_ruta, "Auto", origen=origen_ruta),
                use_container_width=True,
            )
            st.link_button(
                "Ruta según tu preferencia",
                crear_ruta(destino_ruta, plan["transporte"], origen=origen_ruta),
                use_container_width=True,
            )

        st.markdown("### Eventos y actividades especiales")
        st.write(
            "También podés descubrir ferias, festivales, recorridos, talleres y eventos deportivos "
            "que se organicen cerca de la fecha de tu salida."
        )
        fecha_evento = date.fromisoformat(plan["fecha"]).strftime("%d/%m/%Y")
        consulta_eventos = urlencode({
            "q": f"eventos actividades {plan['zona']} {fecha_evento} agenda oficial"
        })
        st.link_button(
            "Buscar eventos para esa fecha y zona",
            "https://www.google.com/search?" + consulta_eventos,
            use_container_width=True,
        )
        st.link_button(
            "Explorar agenda oficial de Buenos Aires",
            "https://turismo.buenosaires.gob.ar/es/que-hacer-en-la-ciudad",
            use_container_width=True,
        )
        st.caption(
            "Los eventos cambian según la fecha y el lugar. Revisá la página oficial del organizador "
            "para confirmar fecha, inscripción, entradas y posibles cambios."
        )

        if plan["ver_clima"]:
            st.markdown("###  Pronóstico del tiempo")

            fecha_elegida = date.fromisoformat(plan["fecha"])
            dias = (fecha_elegida - date.today()).days

            if 0 <= dias <= 15:
                with st.spinner("Consultando el pronóstico..."):
                    clima = consultar_clima(
                        plan["zona"],
                        fecha_elegida,
                    )

                if clima and "error" not in clima:
                    st.markdown(
                        f'''<div style="background:linear-gradient(130deg,#E8F2FF 0%,#F4F0FF 100%); border:1px solid #D9E4FA; border-radius:22px; padding:22px 24px; margin:8px 0 16px 0;">
                            <div style="font-size:0.78rem; font-weight:900; letter-spacing:1.5px; color:#5574A9; text-transform:uppercase;">Pronóstico para tu salida</div>
                            <div style="font-size:1.65rem; font-weight:900; color:#263F73; margin-top:5px;">{clima['descripcion']}</div>
                            <div style="font-size:0.95rem; color:#5B6E8C; margin-top:3px;">{clima.get('lugar', plan['zona'])} · {fecha_elegida.strftime('%d/%m/%Y')}</div>
                        </div>''',
                        unsafe_allow_html=True,
                    )
                    cc1, cc2, cc3 = st.columns(3)
                    cc1.metric("Temperatura máxima", f"{clima['max']} °C")
                    cc2.metric("Temperatura mínima", f"{clima['min']} °C")
                    cc3.metric(
                        "Probabilidad de lluvia",
                        f"{int(clima['lluvia'])}%" if clima["lluvia"] is not None else "Sin dato",
                    )
                    if clima["lluvia"] is not None:
                        st.progress(
                            max(0, min(100, int(clima["lluvia"]))) / 100,
                            text="Probabilidad de lluvia",
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

        st.markdown("###  Tu plan alternativo")

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
                f"{CATEGORIAS.get(plan.get('categoria_original', plan['actividad']), plan['actividad'])} y "
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

        st.markdown("### Compartir este plan")
        st.write("Generá un vínculo para mandárselo a tu amiga o a tu grupo. Quien lo abra podrá ver los detalles y abrir el destino en Google Maps.")
        fecha_compartir = date.fromisoformat(plan["fecha"]).strftime("%d/%m/%Y")
        datos_para_compartir = {
            "actividad": plan.get("actividad", "Salida"),
            "lugar": plan.get("lugar", ""),
            "zona": plan.get("zona", ""),
            "fecha_mostrar": fecha_compartir,
            "hora_exacta": plan.get("hora_exacta", "A definir"),
            "hora": plan.get("hora", "A definir"),
            "con_quien": plan.get("con_quien", ""),
            "notas": plan.get("notas", ""),
        }
        codigo_compartir = base64.urlsafe_b64encode(
            json.dumps(datos_para_compartir, ensure_ascii=False).encode("utf-8")
        ).decode("ascii")
        url_compartir = "https://aplicacinplanly-fzdgevludiwfnrmkruamjo.streamlit.app/?plan_compartido=" + quote(codigo_compartir, safe="")
        st.code(url_compartir, language=None)
        st.caption("Usá el botón de copiar del recuadro para copiar el vínculo y mandárselo a tu amiga. El enlace comparte una copia de los datos actuales; si editás el plan después, generá un vínculo nuevo.")

        st.markdown("###  Guardar tu idea")

        if st.button(
            "Guardar este plan en favoritos",
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
    st.markdown("## Tus favoritos ")

    st.write(
        "Acá encontrás los lugares y las ideas que guardaste."
    )

    if not st.session_state.favoritos:
        vacio_texto, vacio_momi = st.columns([1.7, 1], gap="large", vertical_alignment="center")
        with vacio_texto:
            st.markdown("""
        <div class="section-card">
            <h3>Tu lista está esperando nuevas ideas</h3>
            <p>Entrá en «Explorar» y guardá los lugares que te gusten.</p>
        </div>
        """, unsafe_allow_html=True)
        with vacio_momi:
            mostrar_momi(8)

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
                        "Ver en Google Maps",
                        favorito["url"],
                    )

                with accion:
                    if st.button(
                        "Quitar",
                        key=f"quitar_favorito_{i}",
                    ):
                        st.session_state.favoritos.pop(i)
                        try:
                            guardar_datos_firestore(
                                st.session_state.planes,
                                st.session_state.favoritos,
                            )
                        except Exception:
                            st.warning(
                                "Se quitó de esta sesión, pero no pudimos "
                                "sincronizar el cambio con tu cuenta."
                            )
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
                    + dinero(plan_guardado.get("gasto_total", 0))
                )

                indice_real_hist = len(st.session_state.planes) - 1 - i
                col_detalle_hist, col_mapa_hist, col_borrar_hist = st.columns([1.15, 1, 0.8])
                with col_detalle_hist:
                    if st.button("Ver todos los detalles", key=f"historial_detalle_{i}", use_container_width=True):
                        st.session_state.plan_seleccionado_guardado = indice_real_hist
                with col_mapa_hist:
                    st.link_button(
                        "Ver en el mapa",
                        url_maps_plan(plan_guardado),
                        use_container_width=True,
                    )
                with col_borrar_hist:
                    if st.button("🗑️ Eliminar", key=f"historial_eliminar_{i}", use_container_width=True):
                        st.session_state.plan_pendiente_eliminar = indice_real_hist



# =========================================================
# 12. VENTANA DE DETALLES DEL PLAN SELECCIONADO
# =========================================================

seleccionado = st.session_state.get("plan_seleccionado_guardado")
if isinstance(seleccionado, int) and 0 <= seleccionado < len(st.session_state.planes):
    mostrar_detalle_plan_guardado(st.session_state.planes[seleccionado], "guardado")


if st.session_state.get("aviso_plan_eliminado"):
    st.success("Plan eliminado de tu historial.")
    st.session_state.aviso_plan_eliminado = False

indice_pendiente = st.session_state.get("plan_pendiente_eliminar")
if isinstance(indice_pendiente, int):
    confirmar_eliminar_plan(indice_pendiente)


# =========================================================
# 13. PIE DE PÁGINA
# =========================================================

st.markdown("---")

st.markdown("""
<div style="text-align:center; padding:12px;">
    <p style="color:#64748B;">
        PLANLY · Encontrá tu próxima aventura 
    </p>
</div>
""", unsafe_allow_html=True)
