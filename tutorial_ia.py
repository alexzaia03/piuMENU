"""
Tutorial: Come usare l'IA in Python con chiave API da .env

Questo è un esempio generico che mostra come:
1. Caricare una chiave API da un file .env
2. Usare Google Gemini per generare contenuto
"""

import os
import sys

# ============================================================
# PASSO 1: Carica le variabili d'ambiente dal file .env
# ============================================================
# Il file .env deve contenere: GOOGLE_API_KEY=tua_chiave_qui


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


# Recupera la chiave API
load_env_file()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ Errore: non hai impostato GOOGLE_API_KEY nel file .env")
    print("Crea un file .env con il contenuto: GOOGLE_API_KEY=la_tua_chiave")
    exit(1)

MODEL_NAME = "gemini-2.5-flash"

# Preferisci il nuovo SDK; fallback al legacy solo se necessario.
try:
    from google import genai as new_genai  # google-genai
except ImportError:
    new_genai = None

if new_genai is None:
    import google.generativeai as legacy_genai  # type: ignore[reportMissingImports]
    legacy_genai.configure(api_key=api_key)
    client = legacy_genai.GenerativeModel(MODEL_NAME)
else:
    client = new_genai.Client(api_key=api_key)


def generate_content(prompt_text: str):
    """Genera contenuto con SDK nuovo o legacy."""
    if new_genai is not None:
        return client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt_text,
        )
    return client.generate_content(prompt_text)


def fail_with_help(error: Exception) -> None:
    """Mostra errori API in modo leggibile e termina."""
    message = str(error)
    if "reported as leaked" in message.lower() or "permissiondenied" in message.lower():
        print("❌ API key rifiutata (403): la chiave risulta compromessa o non valida.")
        print("1) Revoca la chiave in Google AI Studio")
        print("2) Crea una nuova chiave")
        print("3) Aggiorna .env: GOOGLE_API_KEY=nuova_chiave")
    else:
        print(f"❌ Errore API: {error}")
    sys.exit(1)

# ============================================================
# Esempio 3: Analisi di dati (es. lista ingredienti)
print("\n--- Esempio 3: Analisi ingredienti ---")
ingredienti = ["pomodori", "mozzarella", "basilico", "olio d'oliva"]
#richiesta
prompt = f"Data questa lista di ingredienti: {ingredienti}. Che piatto consiglieresti di preparare? Rispondi in italiano."

#risposta
try:
    response = generate_content(prompt)
except Exception as e:
    fail_with_help(e)
print(f"🤖 IA consiglia: {response.text}")



# ============================================================
# Esempio 5: Gestione errori
print("\n--- Esempio 5: Gestione errori ---")
try:
    response = generate_content("")  # Prompt vuoto per generare errore
except Exception as e:
    print(f"❌ Errore gestito: {e}")

print("\n✅ Tutorial completato!")



#ciao leo qua
#xxxxxxxxxxxx