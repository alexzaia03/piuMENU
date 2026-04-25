"""
Interfaccia utente per l'IA culinaria con Streamlit

Permette all'utente di inserire ingredienti e ricevere suggerimenti ricette dall'IA.
"""

import os
import sys
import streamlit as st

# ============================================================
# Configurazione Streamlit
# ============================================================
st.set_page_config(
    page_title="Chef IA - Consigli Ricette",
    page_icon="🍳",
    layout="centered"
)

# ============================================================
# Carica variabili d'ambiente
# ============================================================
def load_env_file(path: str = ".env") -> None:
    """Carica variabili KEY=VALUE da un file .env semplice."""
    if not os.path.exists(path):
        return

    with open(path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


load_env_file()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ Chiave API non configurata. Modifica il file .env")
    st.stop()

MODEL_NAME = "gemini-2.5-flash"

# Inizializza client Google
try:
    from google import genai as new_genai
    client = new_genai.Client(api_key=api_key)
    use_new_sdk = True
except ImportError:
    import google.generativeai as legacy_genai
    legacy_genai.configure(api_key=api_key)
    client = legacy_genai.GenerativeModel(MODEL_NAME)
    use_new_sdk = False


def generate_content(prompt_text: str):
    """Genera contenuto con l'IA."""
    if use_new_sdk:
        return client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt_text,
        )
    return client.generate_content(prompt_text)


# ============================================================
# Interfaccia utente
# ============================================================
st.title("🍳 Chef IA")
st.markdown("Inserisci gli ingredienti che hai a disposizione e l'IA ti suggerirà una ricetta!")

# Input ingredienti
ingredienti_input = st.text_area(
    "📝 I tuoi ingredienti:",
    placeholder="es: uova, pomodoro, mozzarella, basilico",
    height=100
)

# Pulsante invio
if st.button("🔍 Suggerisci ricetta", type="primary"):
    if not ingredienti_input.strip():
        st.warning("⚠️ Inserisci almeno un ingrediente!")
    else:
        with st.spinner("🤔 L'IA sta pensando..."):
            try:
                prompt = f"""Sei un chef esperto italiano. 
L'utente ha questi ingredienti: {ingredienti_input}

Suggerisci una o più ricette che può preparare con questi ingredienti.
Per ogni ricetta indica:
- Nome del piatto
- Breve descrizione
- Procedimento sintetico

Rispondi in italiano in modo chiaro e amichevole."""

                response = generate_content(prompt)
                
                st.success("🍽️ Ecco i suggerimenti:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"❌ Errore: {e}")

# ============================================================
# Footer
# ============================================================
st.markdown("---")
st.caption("💡 Powered by Google Gemini • piuMENU")